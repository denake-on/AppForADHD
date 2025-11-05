import requests
import json
import re
from typing import List, Dict, Any
import os

class TaskBreakdownService:
    def __init__(self):
        # OpenRouter API配置
        self.api_key = os.getenv('OPENROUTER_API_KEY', 'your_default_api_key_here')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "tngtech/deepseek-r1t-chimera:free"
        
    def call_openrouter_api(self, prompt: str, task_info: Dict[str, Any]) -> str:
        """
        调用OpenRouter API进行任务拆解
        """
        # 构建系统提示词
        system_prompt = """你是一个专业的项目管理助手，擅长将复杂任务拆解为可执行的子任务。

请根据用户提供的任务信息和拆解要求，将任务拆解为具体的、可执行的子任务，拆解的具体数量视任务复杂度和用户要求决定。

要求：
1. 每个子任务应该是具体、可执行的步骤
2. 子任务之间应该有逻辑顺序
3. 每个子任务应该包含明确的行动描述
4. 子任务应该与原始任务的层级相匹配
5. 为每个子任务设置合理的截止日期和优先级
6. 输出格式为JSON数组，每个子任务包含title、description、deadline和priority字段

优先级说明：
- "high": 高优先级（紧急且重要）
- "medium": 中优先级（重要但不紧急，或紧急但不重要）
- "low": 低优先级（既不紧急也不重要）

截止日期格式：YYYY-MM-DD（相对于当前日期的合理时间安排）

示例输出格式(根据任务复杂度和用户要求决定拆解数量)：
[
  {
    "title": "子任务1标题",
    "description": "子任务1的详细描述",
    "deadline": "2024-01-15",
    "priority": "high"
  },
  {
    "title": "子任务2标题", 
    "description": "子任务2的详细描述",
    "deadline": "2024-01-20",
    "priority": "medium"
  },
  {
    "title": "子任务3标题", 
    "description": "子任务3的详细描述",
    "deadline": "2024-01-25",
    "priority": "low"
  }
]"""

        # 获取当前日期
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 构建用户提示词
        user_prompt = f"""
当前日期：{current_date}

原始任务信息：
- 任务标题：{task_info['title']}
- 任务描述：{task_info['description']}
- 任务层级：Level {task_info['level']}
- 任务优先级：{task_info['priority']}
- 截止日期：{task_info['deadline']}

用户拆解要求：
{prompt}

请根据以上信息，将任务拆解为合适的子任务。注意：
1. 根据原始任务的截止日期和当前日期，为每个子任务设置合理的时间安排
2. 考虑任务之间的依赖关系，合理安排截止日期
3. 根据子任务的重要性和紧急性设置优先级
4. 以JSON格式返回，包含title、description、deadline和priority字段
5. 请严格遵守JSON格式，不要添加任何其他内容,禁止返回其他任何内容和错误格式
"""

        # 构建请求数据
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": user_prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 4000
        }

        # 设置请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",  # 可选：标识请求来源
            "X-Title": "WeiWan Task Breakdown"  # 可选：应用名称
        }

        try:
            # 发送请求
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                error_msg = f"API请求失败: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return None
                
        except requests.exceptions.RequestException as e:
            error_msg = f"请求异常: {str(e)}"
            print(f"❌ {error_msg}")
            return None
        except Exception as e:
            error_msg = f"处理异常: {str(e)}"
            print(f"❌ {error_msg}")
            return None

    def parse_breakdown_result(self, api_response: str) -> List[Dict[str, str]]:
        """
        解析API返回的拆解结果
        """
        print("📄 API原始响应:")
        print(api_response)
        print("="*50)
        
        try:
            # 清理响应内容
            cleaned_response = api_response.strip()
            
            # 尝试提取JSON部分 - 使用更宽松的正则表达式
            patterns = [
                r'\[.*?\]',  # 标准JSON数组
                r'```json\s*(\[.*?\])\s*```',  # Markdown代码块
                r'```\s*(\[.*?\])\s*```',  # 代码块
            ]
            
            for i, pattern in enumerate(patterns):
                json_match = re.search(pattern, cleaned_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1) if i > 0 else json_match.group()
                    print(f"🔍 找到JSON字符串 (模式{i+1})，长度: {len(json_str)}")
                    try:
                        result = json.loads(json_str)
                        print(f"✅ 解析成功，获得 {len(result)} 个子任务")
                        return result
                    except json.JSONDecodeError as e:
                        print(f"⚠️ 模式{i+1}解析失败: {str(e)}")
                        continue
                    
            # 尝试直接解析JSON
            if cleaned_response.startswith('['):
                # 找到第一个完整的JSON数组结束位置
                bracket_count = 0
                end_idx = -1
                for i, char in enumerate(cleaned_response):
                    if char == '[':
                        bracket_count += 1
                    elif char == ']':
                        bracket_count -= 1
                        if bracket_count == 0:
                            end_idx = i + 1
                            break
                
                if end_idx > 0:
                    json_str = cleaned_response[:end_idx]
                    print(f"🔍 提取JSON数组，长度: {len(json_str)}")
                    result = json.loads(json_str)
                    print(f"✅ 直接解析成功，获得 {len(result)} 个子任务")
                    return result
            
            # 尝试修复截断的JSON
            print("🔧 尝试修复截断的JSON...")
            fixed_json = self.fix_truncated_json(cleaned_response)
            if fixed_json:
                try:
                    result = json.loads(fixed_json)
                    print(f"✅ 修复后解析成功，获得 {len(result)} 个子任务")
                    return result
                except json.JSONDecodeError as e:
                    print(f"⚠️ 修复后仍然解析失败: {str(e)}")
            
            # 如果无法解析JSON，返回原始文本
            print("⚠️ 所有解析方法都失败")
            return [{"title": "解析失败", "description": api_response}]
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON解析失败: {str(e)}")
            return [{"title": "解析失败", "description": api_response}]
        except Exception as e:
            print(f"⚠️ 解析异常: {str(e)}")
            return [{"title": "解析异常", "description": api_response}]
    
    def fix_truncated_json(self, text: str) -> str:
        """
        尝试修复截断的JSON
        """
        try:
            # 查找JSON开始位置
            start_idx = text.find('[')
            if start_idx == -1:
                return None
            
            # 从开始位置提取到文本末尾
            json_part = text[start_idx:]
            
            # 尝试找到最后一个完整的对象
            brace_count = 0
            last_complete_idx = -1
            
            for i, char in enumerate(json_part):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        last_complete_idx = i
            
            if last_complete_idx > 0:
                # 截取到最后一个完整对象
                complete_json = json_part[:last_complete_idx + 1] + ']'
                print(f"🔧 修复后的JSON长度: {len(complete_json)}")
                return complete_json
            
            return None
        except Exception as e:
            print(f"⚠️ 修复JSON时出错: {str(e)}")
            return None

    def breakdown_task(self, task_info: Dict[str, Any], user_prompt: str) -> List[Dict[str, str]]:
        """
        主要拆解任务方法
        """
        print(f"\n🤖 开始AI拆解任务: {task_info['title']}")
        
        # 调用OpenRouter API
        api_response = self.call_openrouter_api(user_prompt, task_info)
        
        if api_response is None:
            print("❌ API调用失败")
            return []
        
        print("✅ API调用成功")
        
        # 解析结果
        breakdown_tasks = self.parse_breakdown_result(api_response)
        
        # 检查解析结果
        if not breakdown_tasks or (len(breakdown_tasks) == 1 and breakdown_tasks[0].get('title') in ['解析失败', '解析异常', '原始响应']):
            print("❌ 拆解失败")
            return []
        
        print(f"✅ 拆解成功，获得 {len(breakdown_tasks)} 个子任务")
        
        return breakdown_tasks


# 创建全局实例
breakdown_service = TaskBreakdownService()

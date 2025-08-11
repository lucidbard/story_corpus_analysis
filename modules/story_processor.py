from modules.llm_provider import LLMProvider
from modules.data_models import Scene, Goal
import re, json

class SimpleStoryProcessor:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def analyze_story(self, story_text, story_id="story"):
        prompt = f"""Analyze this story text and identify natural scene breaks.\nText to analyze:\n{story_text}\nReturn JSON with this structure:\n{{\n  'scenes': [{{'scene_id': 'scene_1', 'description': 'Brief description', 'text': 'Scene text'}}]\n}}"""
        if not self.llm.client:
            return []
        response = self.llm.client.generate(model=self.llm.model, prompt=prompt, options={'num_predict': 2000, 'temperature': 0.3, 'num_ctx': 16000})
        response_text = response['response']
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            scenes = [Scene(scene_id=f"{story_id}_scene_{i+1}", book_id=story_id, chapter_num=1, scene_num=i+1, text=s.get('text', '')) for i, s in enumerate(data.get('scenes', []))]
            return scenes
        return []

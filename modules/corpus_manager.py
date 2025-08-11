from pathlib import Path
from modules.story_processor import SimpleStoryProcessor

def process_entire_corpus(data_dir, processor):
    corpus_path = Path(data_dir)
    txt_files = list(corpus_path.glob("*.txt"))
    all_results = {}
    for book_file in txt_files:
        book_id = book_file.stem
        with open(book_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        scenes = processor.analyze_story(text, book_id)
        if scenes:
            all_results[book_id] = {
                'scenes': scenes,
                'book_title': book_id.replace('_', ' ').title(),
                'scene_count': len(scenes)
            }
    return all_results

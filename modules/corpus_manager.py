from pathlib import Path
from modules.story_processor import SimpleStoryProcessor

def process_entire_corpus(data_dir, processor, sample_size=None):
    corpus_path = Path(data_dir)
    txt_files = list(corpus_path.glob("*.txt"))
    
    # Sort files alphabetically for consistent processing order
    txt_files.sort(key=lambda x: x.name)
    
    # Apply sample size if specified
    if sample_size and sample_size < len(txt_files):
        txt_files = txt_files[:sample_size]
    
    all_results = {}
    for book_file in txt_files:
        book_id = book_file.stem
        with open(book_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        # Three-phase processing returns {"scenes": [...], "goals": [...], "conflicts": [...]}
        result = processor.analyze_story(text, book_id)
        
        if result and result.get('scenes'):
            scenes = result['scenes']
            goals = result.get('goals', [])
            conflicts = result.get('conflicts', [])
            
            all_results[book_id] = {
                'scenes': scenes,
                'goals': goals,
                'conflicts': conflicts,
                'book_title': book_id.replace('_', ' ').title(),
                'scene_count': len(scenes),
                'goal_count': len(goals),
                'conflict_count': len(conflicts)
            }
    return all_results

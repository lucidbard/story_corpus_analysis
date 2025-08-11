import json
from pathlib import Path

def prepare_visualization_data(results_dict):
    visualization_data = {
        "metadata": {
            "generated_date": "2025-08-11",
            "total_books": len(results_dict),
            "total_scenes": sum(r['scene_count'] for r in results_dict.values()),
            "processor": "SimpleStoryProcessor"
        },
        "books": []
    }
    for book_id, book_data in results_dict.items():
        book_viz = {
            "book_id": book_id,
            "title": book_data['book_title'],
            "scene_count": book_data['scene_count'],
            "scenes": []
        }
        for scene in book_data['scenes']:
            scene_viz = {
                "scene_id": scene.scene_id,
                "scene_num": scene.scene_num,
                "text_preview": scene.text[:200] + "..." if len(scene.text) > 200 else scene.text,
                "text_length": len(scene.text),
                "chapter": scene.chapter_num
            }
            book_viz["scenes"].append(scene_viz)
        visualization_data["books"].append(book_viz)
    return visualization_data

def export_for_html_visualization(visualization_data, filename="scene_analysis_visualization.json"):
    output_file = Path(filename)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(visualization_data, f, indent=2, ensure_ascii=False)
    return output_file

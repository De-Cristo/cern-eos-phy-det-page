import os
import argparse
import json
import logging
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size // 5]) # Approximation since size is char-based
        # Let's do character based to be safe
        break
    
    # Character based chunking
    chunks_str = []
    i = 0
    text_len = len(text)
    while i < text_len:
        end = min(i + chunk_size, text_len)
        # Try to break at a space
        if end < text_len:
            last_space = text.rfind(" ", i, end)
            if last_space != -1 and last_space > i + chunk_size // 2:
                end = last_space
        chunks_str.append(text[i:end].strip())
        if end == text_len:
            break
        i = end - overlap
        if i < 0:
            break
    
    return [c for c in chunks_str if c]

def extract_text(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if filepath.endswith('.html') or filepath.endswith('.htm'):
            soup = BeautifulSoup(content, "html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text(separator=" ")
            return " ".join(text.split())
        else:
            return " ".join(content.split())
    except Exception as e:
        logging.warning(f"Failed to extract text from {filepath}: {e}")
        return ""

def main():
    parser = argparse.ArgumentParser(description="Build RAG Index")
    parser.add_argument("--root", required=True, help="Root directory to scan")
    parser.add_argument("--out-dir", required=True, help="Output directory for ai_index")
    parser.add_argument("--base-url", required=True, help="Base URL for the website")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.root)
    out_dir = os.path.abspath(args.out_dir)
    base_url = args.base_url.rstrip("/")
    
    os.makedirs(out_dir, exist_ok=True)
    chunks_file = os.path.join(out_dir, "chunks.jsonl")
    manifest_file = os.path.join(out_dir, "manifest.json")

    allowed_exts = {".html", ".htm", ".md", ".txt", ".csv", ".json"}
    
    scanned_count = 0
    indexed_count = 0
    chunk_count = 0
    skipped_count = 0

    with open(chunks_file, 'w', encoding='utf-8') as cf:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip hidden dirs and ai_index
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'ai_index']
            
            for filename in filenames:
                scanned_count += 1
                if filename.startswith('.'):
                    skipped_count += 1
                    continue
                
                ext = os.path.splitext(filename)[1].lower()
                if ext not in allowed_exts:
                    skipped_count += 1
                    continue
                
                filepath = os.path.join(dirpath, filename)
                
                if not os.path.exists(filepath):
                    skipped_count += 1
                    continue
                
                size = os.path.getsize(filepath)
                if size > 2 * 1024 * 1024: # Skip files > 2MB to prevent OOM
                    logging.warning(f"Skipping {filepath} (Too large: {size} bytes)")
                    skipped_count += 1
                    continue

                rel_path = os.path.relpath(filepath, root_dir)
                
                # Infer source URL
                url_path = rel_path.replace(os.sep, "/")
                if url_path.endswith("index.html"):
                    url_path = url_path[:-10]
                elif url_path == "index.html":
                    url_path = ""
                source_url = f"{base_url}/{url_path}"

                text = extract_text(filepath)
                if not text:
                    skipped_count += 1
                    continue
                
                mtime = os.path.getmtime(filepath)
                chunks = chunk_text(text)
                
                for idx, chunk in enumerate(chunks):
                    chunk_id = f"{rel_path}_{idx}"
                    chunk_data = {
                        "chunk_id": chunk_id,
                        "title": filename,
                        "source_path": rel_path,
                        "source_url": source_url,
                        "file_type": ext.lstrip("."),
                        "mtime": mtime,
                        "text": chunk
                    }
                    cf.write(json.dumps(chunk_data) + "\n")
                    chunk_count += 1
                
                indexed_count += 1

    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "scanned_files": scanned_count,
        "indexed_files": indexed_count,
        "chunks_written": chunk_count,
        "skipped_files": skipped_count
    }
    
    with open(manifest_file, 'w', encoding='utf-8') as mf:
        json.dump(manifest, mf, indent=2)

    logging.info(f"Scanned files: {scanned_count}")
    logging.info(f"Indexed files: {indexed_count}")
    logging.info(f"Chunks written: {chunk_count}")
    logging.info(f"Skipped files: {skipped_count}")

if __name__ == "__main__":
    main()

import os
from pathlib import Path


def compile_folder_data_to_md(root_dir: str, output_md_path: str):
    root = Path(root_dir)
    if not root.exists() or not root.is_dir():
        print(f"Error: The directory '{root_dir}' does not exist.")
        return

    markdown_lines = []
    markdown_lines.append(f"# Benchmark Summary: {root.name}\n")
    markdown_lines.append(
        "This file contains compiled logs and CSV data from the benchmark directories.\n"
    )
    markdown_lines.append("---")

    # Walk through all subdirectories
    for dirpath, _, filenames in os.walk(root):
        current_dir = Path(dirpath)

        # Skip the root directory itself if it contains no relevant files directly
        if current_dir == root and not any(
            f.endswith((".csv", ".txt")) for f in filenames
        ):
            continue

        # Check if there are csv or txt files in this specific folder
        target_files = [f for f in filenames if f.endswith((".csv", ".txt"))]

        if target_files:
            # Create a header for the folder (relative path for cleanliness)
            rel_path = current_dir.relative_to(root.parent)
            markdown_lines.append(f"## 📁 Directory: `{rel_path}`\n")

            # Process files (sorting keeps things predictable, e.g., csv then txt)
            for filename in sorted(target_files):
                file_path = current_dir / filename
                markdown_lines.append(f"### 📄 File: `{filename}`")

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()

                    # Format based on file type
                    if filename.endswith(".csv"):
                        markdown_lines.append("```csv")
                        markdown_lines.append(content)
                        markdown_lines.append("```\n")
                    elif filename.endswith(".txt"):
                        markdown_lines.append("```text")
                        markdown_lines.append(content)
                        markdown_lines.append("```\n")

                except Exception as e:
                    markdown_lines.append(
                        f"\n*Error reading file: {str(e)}*\n"
                    )

            markdown_lines.append("---")

    # Write everything to the output markdown file
    with open(output_md_path, "w", encoding="utf-8") as md_file:
        md_file.write("\n".join(markdown_lines))

    print(f"Successfully generated Markdown report at: {output_md_path}")


if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Replace this with the absolute or relative path to your 'Qwen3.5' or 'BENCHMARK-LLM' directory
    ROOT_DIRECTORY = "./Qwen3.5"
    OUTPUT_FILE = "benchmark_summary.md"
    # ---------------------

    compile_folder_data_to_md(ROOT_DIRECTORY, OUTPUT_FILE)
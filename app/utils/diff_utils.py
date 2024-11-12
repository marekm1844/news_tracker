from simplediff import html_diff

def compare_versions(old_content: str, new_content: str) -> str:
    # Generate the diff as HTML
    diff_html = html_diff(old_content, new_content)
    return diff_html
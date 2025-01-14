def markdown_to_blocks(markdown):
    doc = markdown.split("\n")
    result = []
    curr = ""
    for line in doc:
        stripped = line.strip()
        if not stripped:
            if curr:
                result.append(curr)
            curr = ""
        else:
            if curr:
                curr += "\n"
            curr += stripped
    if curr:
        result.append(curr)

    return result

def block_to_block_type(block):
    if block.startswith("#"):
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                if char == " ":
                    return "heading"
                break 

    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    lines = block.split("\n")

    ordered_list = True
    for i, line in enumerate(lines):
        expect_start = f"{i + 1}. "
        if not line.startswith(expect_start):
            ordered_list = False
            break
    if ordered_list:
        return "ordered_list"

    all_quotes = True
    for line in lines:
        if not line.startswith('> '):
            all_quotes = False
            break
    if all_quotes:
        return "quote"
        
    all_unordered = True
    for line in lines:
        if not (line.startswith('* ') or line.startswith('- ')):
            all_unordered = False
            break
    if all_unordered:
        return "unordered_list"

    return "paragraph"


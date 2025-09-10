import os
from dotenv import load_dotenv
from notion_client import Client
from langchain_community.document_loaders import NotionDBLoader

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
START_PAGE_ID = '264120560ff680198c0fefbbe17bfc2c' # 시작 페이지 ID. 나중에 Frontend에서 받아올 것

notion = Client(auth=NOTION_TOKEN)

def get_text_from_block(block: dict) -> str:
    """다양한 블록 타입에서 텍스트를 추출하는 함수"""
    block_type = block["type"]
    
    # 블록 타입에 따라 텍스트가 담긴 위치가 다름
    if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", 
                      "bulleted_list_item", "numbered_list_item", "quote", "callout", "code", "toggle", "breadcrumb"]:
        # 대부분의 텍스트는 해당 타입 이름의 키 값 안에 'rich_text' 배열로 존재
        text_parts = block[block_type].get("rich_text", [])
        
    elif block_type == "to_do":
        text_parts = block["to_do"].get("rich_text", [])
        checked = block["to_do"]["checked"]
        return f"[{'x' if checked else ' '}] {''.join([part['plain_text'] for part in text_parts])}"
        
    elif block_type == "child_page":
        return f"{block['child_page']['title']} (하위 페이지)"

    elif block_type == "child_database":
        child_db_id = block["id"]
        loader = NotionDBLoader(
            integration_token=NOTION_TOKEN,
            database_id=child_db_id,
            request_timeout_sec=120,  # optional, defaults to 10
        )
        docs = loader.load()
        return f"{block['child_database']['title']} (하위 데이터베이스) \n {docs}"

    elif block_type == "bookmark":
        return f"{block['bookmark']['url']} (북마크)"
    
    elif block_type == "table":
        table_block_id = block["id"]
        all_rows_data = [] # 모든 행 데이터를 저장할 리스트

        # 표 블록의 ID를 사용해 자식인 'table_row' 블록들을 가져옵니다.
        table_rows = notion.blocks.children.list(block_id=table_block_id).get("results", [])

        # 각 행(table_row)을 순회하며 셀 데이터를 추출합니다
        for row in table_rows:
            row_cells = row["table_row"]["cells"]
            row_data = [] # 현재 행의 셀 데이터를 저장할 리스트
            
            # 각 셀의 텍스트를 추출합니다.
            for cell in row_cells:
                cell_text = "".join([part["plain_text"] for part in cell])
                row_data.append(cell_text)
            
            all_rows_data.append(row_data)
            
        table_text = ""
        for row_content in all_rows_data:
            table_text += " | ".join(row_content) + "\n"
        
        return table_text
    
    elif block_type == "file":
        return f"{block['file']['name']} (파일)"

    else:
        # 지원하지 않는 블록 타입은 건너뜀 (이미지, 파일 등)
        return ""
        
    # rich_text 배열의 모든 텍스트 조각을 하나로 합침
    return "".join([part["plain_text"] for part in text_parts])

def process_all_content_recursively(parent_id: str, depth: int = 0):
    """
    페이지와 블록의 모든 계층 구조를 재귀적으로 탐색하는 통합 함수
    - parent_id: 페이지 또는 블록의 ID
    - depth: 현재 탐색 깊이 (들여쓰기용)
    """
    indent = "  " * depth
    all_text = ""
    
    try:
        # parent_id에 속한 자식 블록들을 가져옴 (페이지 또는 블록)
        blocks = notion.blocks.children.list(block_id=parent_id).get("results", [])

        for block in blocks:
            # 1. 현재 블록의 내용을 먼저 가져옴
            block_text = get_text_from_block(block)
            if block_text:
                all_text += f"{indent}- {block_text}\n"

            # 2. 이 블록이 '하위 페이지'인지 확인하고 재귀 호출
            if block["type"] == "child_page":
                all_text += process_all_content_recursively(block["id"], depth + 1)
            
            # 3. '하위 페이지'가 아니면서 다른 자식 블록(들여쓰기)을 가졌는지 확인하고 재귀 호출
            elif block["has_children"]:
                all_text += process_all_content_recursively(block["id"], depth + 1)

    except Exception as e:
        all_text += f"{indent}🔥 ID({parent_id}) 처리 중 오류 발생: {e}\n"
        
    return all_text


# --- 스크립트 실행 ---
if __name__ == "__main__":
    try:
        start_page_info = notion.pages.retrieve(page_id=START_PAGE_ID)
        start_page_title_parts = start_page_info["properties"]["title"]["title"]
        start_page_title = start_page_title_parts[0]["plain_text"] if start_page_title_parts else "(제목 없음)"

        print(f"탐색 시작: {start_page_title} (ID: {START_PAGE_ID})\n" + "="*40)
        result = process_all_content_recursively(START_PAGE_ID)
        print(result)
        print("="*40 + "\n탐색 완료.")
        
    except Exception as e:
        print(f"🔥 시작 페이지({START_PAGE_ID})에 접근할 수 없습니다: {e}")
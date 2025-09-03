"""
Tool Registry - 모든 Tool들을 등록하고 관리하는 중앙 레지스트리
"""

from typing import Dict, Any, List, Callable
import asyncio

from .mcp_adapter import (
    GoogleDriveAdapter,
    GoogleCalendarAdapter,
    NotionAdapter,
    SlackAdapter,
)
from .rag_tool import RAGTool


class ToolRegistry:
    """Tool Registry 클래스"""

    def __init__(self):
        self.tools: Dict[str, Any] = {}
        self.adapters: Dict[str, Any] = {}

    async def initialize(self):
        """Tool Registry 초기화"""
        # MCP Adapters 초기화 (실제 MCP 서버는 나중에 연결)
        print("Tool Registry 초기화 중...")

        # RAG Tool 등록
        rag_tool = RAGTool()
        await self._register_rag_tool(rag_tool)

        print("Tool Registry 초기화 완료")

    async def register_mcp_adapters(self, mcp_servers: Dict[str, Any]):
        """MCP Adapters 등록"""
        if "google_drive" in mcp_servers:
            adapter = GoogleDriveAdapter(mcp_servers["google_drive"])
            await adapter.connect()
            self.adapters["google_drive"] = adapter
            await self._register_adapter_tools("google_drive", adapter)

        if "google_calendar" in mcp_servers:
            adapter = GoogleCalendarAdapter(mcp_servers["google_calendar"])
            await adapter.connect()
            self.adapters["google_calendar"] = adapter
            await self._register_adapter_tools("google_calendar", adapter)

        if "notion" in mcp_servers:
            adapter = NotionAdapter(mcp_servers["notion"])
            await adapter.connect()
            self.adapters["notion"] = adapter
            await self._register_adapter_tools("notion", adapter)

        if "slack" in mcp_servers:
            adapter = SlackAdapter(mcp_servers["slack"])
            await adapter.connect()
            self.adapters["slack"] = adapter
            await self._register_adapter_tools("slack", adapter)

    async def _register_adapter_tools(self, adapter_name: str, adapter):
        """Adapter의 Tool들을 등록"""
        tool_definitions = adapter.get_tool_definitions()

        for tool_def in tool_definitions:
            tool_name = tool_def["name"]
            self.tools[tool_name] = {
                "definition": tool_def,
                "adapter": adapter,
                "executor": adapter.execute_tool,
            }
            print(f"Tool 등록됨: {tool_name}")

    async def _register_rag_tool(self, rag_tool):
        """RAG Tool 등록"""
        tool_definitions = rag_tool.get_tool_definitions()

        for tool_def in tool_definitions:
            tool_name = tool_def["name"]
            self.tools[tool_name] = {
                "definition": tool_def,
                "adapter": rag_tool,
                "executor": rag_tool.execute_tool,
            }
            print(f"RAG Tool 등록됨: {tool_name}")

    def get_all_tools(self) -> List[Dict[str, Any]]:
        """등록된 모든 Tool 정의 반환"""
        return [tool["definition"] for tool in self.tools.values()]

    def get_tool_definition(self, tool_name: str) -> Dict[str, Any]:
        """특정 Tool 정의 반환"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")
        return self.tools[tool_name]["definition"]

    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Tool 실행"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")

        tool_info = self.tools[tool_name]
        executor = tool_info["executor"]

        try:
            return await executor(tool_name, **kwargs)
        except Exception as e:
            print(f"Tool 실행 오류 ({tool_name}): {e}")
            raise

    def list_tools(self) -> List[str]:
        """등록된 Tool 이름 목록 반환"""
        return list(self.tools.keys())

    def get_tools_by_category(self, category: str) -> List[str]:
        """카테고리별 Tool 목록 반환"""
        tools = []
        for tool_name in self.tools.keys():
            if tool_name.startswith(category):
                tools.append(tool_name)
        return tools


# 전역 Tool Registry 인스턴스
tool_registry = ToolRegistry()

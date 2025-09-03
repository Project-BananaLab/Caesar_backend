"""
LangGraph 기반 워크플로우 (팀원 담당 영역)
"""

from typing import Dict, Any, List
import asyncio
from datetime import datetime

from tools.tool_registry import tool_registry


class WorkflowEngine:
    """LangGraph 기반 워크플로우 엔진"""

    def __init__(self):
        self.workflows = {}
        self.running_workflows = {}

    async def initialize(self):
        """워크플로우 엔진 초기화"""
        print("워크플로우 엔진 초기화 중...")

        # 기본 워크플로우 등록
        await self._register_default_workflows()

        print("워크플로우 엔진 초기화 완료")

    async def _register_default_workflows(self):
        """기본 워크플로우 등록"""
        # 회의실 예약 → 슬랙 알림 → 노션 기록 워크플로우
        self.workflows["meeting_reservation"] = {
            "name": "회의실 예약 워크플로우",
            "description": "회의실 예약 후 슬랙 알림 및 노션 기록",
            "steps": [
                {
                    "action": "reserve_meeting_room",
                    "tool": "google_calendar_create_event",
                },
                {"action": "notify_slack", "tool": "slack_send_message"},
                {"action": "record_notion", "tool": "notion_create_page"},
            ],
        }

        # 문서 공유 워크플로우
        self.workflows["document_sharing"] = {
            "name": "문서 공유 워크플로우",
            "description": "Google Drive 문서 업로드 후 슬랙 공유",
            "steps": [
                {"action": "upload_document", "tool": "google_drive_upload_file"},
                {"action": "share_document", "tool": "google_drive_share_file"},
                {"action": "notify_slack", "tool": "slack_send_message"},
            ],
        }

    async def execute_workflow(
        self, workflow_name: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """워크플로우 실행"""
        if workflow_name not in self.workflows:
            raise ValueError(f"워크플로우를 찾을 수 없습니다: {workflow_name}")

        workflow = self.workflows[workflow_name]
        workflow_id = f"{workflow_name}_{datetime.now().isoformat()}"

        print(f"워크플로우 실행 시작: {workflow['name']} (ID: {workflow_id})")

        self.running_workflows[workflow_id] = {
            "workflow": workflow,
            "parameters": parameters,
            "status": "running",
            "results": [],
            "started_at": datetime.now(),
        }

        try:
            results = []

            for step in workflow["steps"]:
                print(f"단계 실행: {step['action']} ({step['tool']})")

                # 도구 실행
                step_result = await self._execute_step(step, parameters, results)
                results.append(step_result)

                # 실패 시 워크플로우 중단
                if not step_result.get("success", False):
                    self.running_workflows[workflow_id]["status"] = "failed"
                    break

            # 성공적으로 완료
            if all(result.get("success", False) for result in results):
                self.running_workflows[workflow_id]["status"] = "completed"

            self.running_workflows[workflow_id]["results"] = results
            self.running_workflows[workflow_id]["completed_at"] = datetime.now()

            return {
                "workflow_id": workflow_id,
                "status": self.running_workflows[workflow_id]["status"],
                "results": results,
            }

        except Exception as e:
            print(f"워크플로우 실행 오류: {e}")
            self.running_workflows[workflow_id]["status"] = "error"
            self.running_workflows[workflow_id]["error"] = str(e)

            return {"workflow_id": workflow_id, "status": "error", "error": str(e)}

    async def _execute_step(
        self,
        step: Dict[str, Any],
        parameters: Dict[str, Any],
        previous_results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """워크플로우 단계 실행"""
        action = step["action"]
        tool_name = step["tool"]

        try:
            # 액션별 파라미터 준비
            tool_params = await self._prepare_step_parameters(
                action, parameters, previous_results
            )

            # 도구 실행
            result = await tool_registry.execute_tool(tool_name, **tool_params)

            return {
                "action": action,
                "tool": tool_name,
                "parameters": tool_params,
                "result": result,
                "success": True,
            }

        except Exception as e:
            print(f"단계 실행 오류 ({action}): {e}")
            return {
                "action": action,
                "tool": tool_name,
                "error": str(e),
                "success": False,
            }

    async def _prepare_step_parameters(
        self,
        action: str,
        base_parameters: Dict[str, Any],
        previous_results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """단계별 파라미터 준비"""
        if action == "reserve_meeting_room":
            return {
                "summary": base_parameters.get("meeting_title", "회의"),
                "start_time": base_parameters.get("start_time"),
                "end_time": base_parameters.get("end_time"),
                "description": base_parameters.get("description", ""),
            }

        elif action == "notify_slack":
            # 이전 결과에서 정보 추출
            meeting_info = ""
            for result in previous_results:
                if result.get("action") == "reserve_meeting_room":
                    meeting_info = f"회의가 예약되었습니다: {result.get('result', {})}"

            return {
                "channel": base_parameters.get("slack_channel", "#general"),
                "text": meeting_info or base_parameters.get("message", "알림"),
            }

        elif action == "record_notion":
            return {
                "parent_id": base_parameters.get("notion_page_id"),
                "title": f"회의 기록 - {base_parameters.get('meeting_title', '제목 없음')}",
                "content": f"회의 정보: {base_parameters}",
            }

        else:
            return base_parameters

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """워크플로우 상태 조회"""
        if workflow_id not in self.running_workflows:
            raise ValueError(f"워크플로우를 찾을 수 없습니다: {workflow_id}")

        return self.running_workflows[workflow_id]

    def list_workflows(self) -> List[Dict[str, Any]]:
        """등록된 워크플로우 목록"""
        return list(self.workflows.values())

    def list_running_workflows(self) -> List[Dict[str, Any]]:
        """실행 중인 워크플로우 목록"""
        return list(self.running_workflows.values())

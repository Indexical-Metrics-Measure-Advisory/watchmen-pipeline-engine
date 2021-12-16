from model.model.pipeline.pipeline import ProcessUnit

from pipeline.monitor.model.pipeline_monitor import UnitRunStatus
from pipeline.core.context.stage_context import StageContext


class UnitContext:
    stageContext: StageContext
    unit: ProcessUnit
    unitStatus: UnitRunStatus

    def __init__(self, stageContext, unit):
        self.stageContext = stageContext
        self.unit = unit
        self.unitStatus = UnitRunStatus()

from model.model.pipeline.pipeline import Stage

from pipeline.monitor.model.pipeline_monitor import StageRunStatus
from pipeline.core.context.pipeline_context import PipelineContext


class StageContext:
    pipelineContext: PipelineContext
    stage: Stage
    stageStatus: StageRunStatus

    def __init__(self, pipelineContext, stage, stageStatus):
        self.pipelineContext = pipelineContext
        self.stage = stage
        self.stageStatus = stageStatus

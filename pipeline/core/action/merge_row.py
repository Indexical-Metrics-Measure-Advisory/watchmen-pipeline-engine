import logging
import time

from pipeline.common.utils.data_utils import get_id_name
from pipeline.core.action.utils import update_retry_callback, update_recovery_callback
from pipeline.core.by.parse_on_parameter import parse_parameter_joint
from pipeline.core.context.action_context import get_variables, ActionContext
from pipeline.core.mapping.parse_mapping import parse_mappings
from pipeline.core.monitor.model.pipeline_monitor import ActionStatus
from pipeline.core.retry.retry_template import retry_template, RetryPolicy
from pipeline.storage.read_topic_data import query_topic_data
from pipeline.storage.write_topic_data import update_topic_data_one
from pipeline.topic.storage.topic_schema_storage import get_topic_by_id

log = logging.getLogger("app." + __name__)


def init(action_context: ActionContext):
    def merge_topic():
        # begin time
        start = time.time()

        # create action status monitor
        status = ActionStatus()
        status.type = "merge-row"
        status.uid = action_context.get_pipeline_id()

        previous_data = action_context.previousOfTriggerData
        current_data = action_context.currentOfTriggerData
        action = action_context.action
        if action.topicId is None:
            raise ValueError("action.topicId is empty {0}".format(action.name))

        pipeline_topic = action_context.unitContext.stageContext.pipelineContext.pipelineTopic
        target_topic = get_topic_by_id(action.topicId)

        variables = get_variables(action_context)

        # if there are aggregate functions, need lock the record to update
        mappings_results, having_aggregate_functions = parse_mappings(action.mapping,
                                                                      target_topic,
                                                                      previous_data,
                                                                      current_data,
                                                                      variables)
        status.value = mappings_results

        where_ = parse_parameter_joint(action.by, current_data, variables, pipeline_topic, target_topic)
        status.by = where_

        trigger_pipeline_data_list = []

        target_data = query_topic_data(where_, target_topic, action_context.get_current_user())
        if target_data is None:
            raise Exception("can't insert data in merge row action ")
        else:
            if target_topic.type == "aggregate":
                args = [mappings_results, where_, target_topic, action_context.get_current_user()]
                retry_callback = (update_retry_callback, args)
                recovery_callback = (update_recovery_callback, args)
                execute_ = retry_template(retry_callback, recovery_callback, RetryPolicy())
                result = execute_()
                trigger_pipeline_data_list.append(result)
            else:
                trigger_pipeline_data_list.append(
                    update_topic_data_one(mappings_results, target_data,
                                          action_context.get_pipeline_id(),
                                          target_data[get_id_name()], target_topic, action_context.get_current_user()))
        status.updateCount = status.updateCount + 1
        elapsed_time = time.time() - start
        status.completeTime = elapsed_time
        return status, trigger_pipeline_data_list

    return merge_topic

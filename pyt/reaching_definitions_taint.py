from .base_cfg import AssignmentNode
from .constraint_table import constraint_table
from .reaching_definitions_base import ReachingDefinitionsAnalysisBase
from pyt.utils.log import enable_logger, logger
enable_logger(to_file='./pyt.log')


class ReachingDefinitionsTaintAnalysis(ReachingDefinitionsAnalysisBase):
    """Reaching definitions analysis rules implemented."""

    def fixpointmethod(self, cfg_node):
        JOIN = self.join(cfg_node)
        logger.debug("JOIN is %s", JOIN)
        # Assignment check
        if isinstance(cfg_node, AssignmentNode):
            logger.debug("An assignment node %s", cfg_node)
            logger.debug("blackbox is %s", cfg_node.blackbox)
            logger.debug("An assignment node %s", type(cfg_node))
            arrow_result = JOIN
            logger.debug("arrow_result is %s", arrow_result)

            # Reassignment check
            if cfg_node.left_hand_side not in\
               cfg_node.right_hand_side_variables:
                arrow_result = self.arrow(JOIN, cfg_node)
                logger.debug("2nd arrow_result is %s", arrow_result)

            arrow_result = arrow_result | self.lattice.el2bv[cfg_node]
            logger.debug("self.lattice.el2bv[cfg_node] is %s", self.lattice.el2bv[cfg_node])
            logger.debug("3rd arrow_result is %s", arrow_result)
            constraint_table[cfg_node] = arrow_result
        # Default case
        else:
            logger.debug("Not an assignment node %s", cfg_node)
            constraint_table[cfg_node] = JOIN

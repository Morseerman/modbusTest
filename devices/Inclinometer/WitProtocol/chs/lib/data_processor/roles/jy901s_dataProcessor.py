# coding:UTF-8
try:
    from Inclinometer.WitProtocol.chs.lib.data_processor.interface.i_data_processor import IDataProcessor
except:
    from devices.Inclinometer.WitProtocol.chs.lib.data_processor.interface.i_data_processor import IDataProcessor

"""
    JY901S数据处理器
"""


class JY901SDataProcessor(IDataProcessor):
    onVarChanged = []
    def onOpen(self, deviceModel):
        pass

    def onClose(self):
        pass

    @staticmethod
    def onUpdate(*args):
        for fun in JY901SDataProcessor.onVarChanged:
            fun(*args)
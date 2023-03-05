import tinytuya
import os

env = os.environ

plug = tinytuya.OutletDevice(
    env['TUYA_DEV_ID'],
    env['TUYA_ADDRESS'],
    env['TUYA_LOCALKEY']
)
plug.set_version(3.3)
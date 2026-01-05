# 例: c_engine.pyで使う場合
from somatic_update import SomaticUpdater

somatic = SomaticUpdater()
text = "うふふー！！！"
tensor, c_value = somatic.update(text)
print("Somatic C更新完了！", tensor, c_value)

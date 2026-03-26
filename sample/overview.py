
import uilib
import tkinter

tk = tkinter.Tk()
tk.title("Sample Window")
ui_root = uilib.ui.layout.UI_Layout(
  [
    [
      (
        uilib.ui.value.UI_Dict(
          {}, #初期状態は空
          add_func=lambda: uilib.ui.value.UI_HardDict( #要素追加時に UI_HardDict を作成する
            {
              "name": uilib.ui.value.UI_Str(""),
              "age": uilib.ui.value.UI_Int(0, (0, 100, 1)),
              "tag": uilib.ui.value.UI_List([], add_func=lambda: uilib.ui.value.UI_Str(""))
            },
            label_table={
              "name": "名前",
              "age": "年齢",
              "tag": "タグ"
            }
          )
        ),
        "sample_dict"
      )
    ],
    [
      (
        uilib.ui.layout.UI_Button(
          "Print value", 
          lambda: print(repr(ui_root.get_value())) #ボタン押下時に設定値を表示する
        ), 
        "", 
        1, 
        1, 
        tkinter.E
      )
    ]
  ],
  as_single_value=True #辞書ではなく単体の値として評価する
)
ui_root.build(tk).pack(padx=10, pady=10) #tkinter ウィジットを作成し配置する
ui_root.load_from_param([
  {
    "abc": {
      "name": "ABC",
      "age": 12,
      "tag": ["AAA", "BBB", ""]
    },
    "def": {
      "name": "",
      "age": 0,
      "tag": []
    }
  }
]) #パラメータからウィジットの状態を復元する
tk.mainloop()

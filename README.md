# 地方議会関連データの収集及び加工処理
![Uploading スクリーンショット 2020-07-20 13.20.11.png…]()


- scrape_go2senkyo.py
  - 議員情報を収集するファイル。
  - 議員情報が掲載されているWebページから必要な情報（議員名や性別、年齢、所属政党など）を自動で収集し、議員リストをCsvファイルへ書き込む処理を行う。

- 高槻市会議録.txt
  - 高槻市平成27年3月5日の定例会会議録。
  - このような形式の会議録を元に以下の処理をそれぞれ行う（自治体によって記録フォーマットが異なっている）。

- Text-Auto-Download.txt
  - 会議録を自動でダウンロードするファイル。
  - 会議録を自動でダウンロードし、txtファイル化及び自治体IDと会議名を自動でファイル名に付与する処理を行う。なお、ゼミ生でもコードの改変ができるようにVBAを用いた。

- Attendance.py
  - 会議に出席した議員を判定するファイル。
  - 処理対象となる会議録に出席している議員とそうでない議員（病欠や死亡を含む）を判別する処理を行う。判別する際は、「高槻市会議録.txt」のような形式の会議録と「scrape_go2senkyo.py」で収集した議員リストを互いに参照し、処理を行う。

- Attandance.json
  - 出席テーブルを作成する際に、Attendance.pyが参照するファイル。
  - 会議録のフォーマットは自治体によって異なるため、それに対応できるように、自治体ごとの特徴が記載されている。

- Hatsugen.py
  - 市議会議員や市長、副市長などの行政側の発言をそれぞれ1レコードに分けるためのファイル。
  - 処理対象となる会議録で発言した内容とその発言をした者の属性を1レコードへ加工するための処理を行う。発言した内容と発言した者は、議事録から抽出を行い、議員の属性（年齢や性別、所属政党、得票数など）は、「scrape_go2senkyo.py」で収集した議員リストを参照し、当該レコードへ付与する処理を行う。

- Hatsugen.json
  - 発言テーブルを作成する際に、Attendance.pyが参照するファイル。
  - 会議録のフォーマットは自治体によって異なるため、それに対応できるように、自治体ごとの特徴が記載されている。

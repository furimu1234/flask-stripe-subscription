# Flask-Stripe-Subscription

## 説明
 ラズパイでdockerを起動し、stripeのサブスクシステムを構築してみた
## 目的
 dockerとstripeのサブスクシステムの勉強


## 環境

### 動作環境
 Raspberry Pi4 4GBモデル

 OS Raspberry Pi OS
   
   Discord BOTサーバーとして使ってた物のリソースが余ってたのでそれを使った

 Docker version 20.10.22, build 3a2c30b

### 開発環境(StripeCLIも)
  windows 11 Mem 8GB
  
  VScode

  Python3.10.8

# 初めに
ラズパイにOSをインストールする方法、stripeのサブスクアイテムの作成や、各キーの取得方法、windowsの環境構築についてはここでは説明していません。

(気が向いたらします)


# ラズパイにDockerをインストール ~ 実行出来るようにするまで

ssh等でラズパイに接続


`sudo apt install docker.io`

しかし、これだけで終わりでは無い。
このままでは、`pi`ユーザーでdockerコマンドを使おうとするとエラーが出る

`pi`ユーザーでdockerを使えるようにする必要がある

`sudo usermod -aG docker`

コマンド実行後、再接続をする。

その後、[こちら](https://stackoverflow.com/questions/70195968/dockerfile-raspberry-pi-python-pip-install-permissionerror-errno-1-operation)のサイトを参考にコマンドを実行

やってる内容は大雑把に、新しい署名鍵を登録し、`buster-backports`をリポジトリに新規追加

`sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138`

`echo 'deb http://httpredir.debian.org/debian buster-backports main contrib non-free' | sudo tee -a /etc/apt/sources.list.d/debian-backports.list`

`sudo apt update`

`sudo apt install libseccomp2 -t buster-backports`

# このリポジトリをクローン

このリポジトリを任意のディレクトリにクローンする

一番簡単なクローン方法は

gitをインストールしてる端末で
`git clone git@github.com:furimu1234/flask-stripe-subscription.git`
と入力する事で出来る

後は、zipをダウンロードして展開する方法もある

# ビルド
ターミナルを開き、`Dockerfile`があるディレクトリに移動する

移動後、`docker build イメージ名 .` と入力

イメージ名は任意の物を。
最後の`.`は`Dcokerfile`があるディレクトリを指している

外部ライブラリを毎回インストールする必要があるので少し時間がかかる

# コンテナを実行
ビルド完了後、`docker run -p 5000:80 -it コンテナ名`

コンテナ名は任意の物を。

`-p 5000:80` 

80はflaskがリッスンしているポート

5000はホスト側のポート

http://localhot:5000/ にアクセスするとdockerの80番ポートにアクセスされる

# テストモードでのサブスクリプションのテスト

これをラズパイで動かすのは非常に大変だったので、この時だけwindowsで試した。

まず、windowsの環境で`src/app.py`を起動


[ここ](https://github.com/stripe/stripe-cli/releases/tag/v1.13.6)から`stripe_1.13.6_windows_x86_64.zip
`をダウンロードし展開。

ターミナルの別タブで、展開したフォルダーまで移動。

`.\stripe login --api-key APIシークレットキー` と入力。
APIシークレットキーは自分のキーに置き換える。
エンターを連打しているとブラウザが開くので、画面にそってクリック

認証が完了したら[ここ](https://stripe.com/docs/webhooks/test)を参考に

` .\stripe listen --forward-to http://localhost:80/webhook`と実行

ここで指定したエンドポイントにStripeのイベントが送信されるようにする。

更にターミナルで別タブを開く

`stripe trigger customer.subscription.created`
`stripe trigger customer.subscription.updated`
`stripe trigger customer.subscription.deleted`

を実行。

flaskのアクセスログを見てみると、`/webhook`にアクセスされてるのが分かる
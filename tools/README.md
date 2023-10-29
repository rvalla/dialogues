![icon](https://gitlab.com/azarte/jaqueludios/-/raw/themoststable/public/assets/img/logo_64.png)
# jaqueludios: tools

Some tools that help me with **jaqueludios**.  

## GameImages()

A simple class to transform a chess game in a series of images. You can configure the background
board and the moves period using a *.json* file.  

```
{
	"name": "test",
	"period": 1, //to decide when to save an image
	"sq_size": 135,
	"size": 1080,
	"background": "img/boardR.png", //the background
	"output_path": "output/test",
	"output_name": "testR", //output name for image files
	"game_path": "games/pgn_source_00001.pgn" //a game in pgn format
}
```


Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).

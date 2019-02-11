const urlBase = "http://192.168.56.10:5000";

Vue.component('v-loading', {
  props: {
    text: {
      default: '　コンパイル中・・・',
      type: String
    },
    show: {
      default: false,
      type: Boolean
    }
  },
  // TODO: ローディング画像を出したい
  template: '<div class="mx-auto" style="width: 200px" v-if="show"><span v-text="text"></span></div>'
});

var uploadDir = new Vue({
  el: '#display',
  delimiters: ['[[', ']]'],
  data: {
    dir: [],
    pdfs: [],
    imgExts: ["png", "jpg", "jpeg", "eps", "pdf"],
    show: false,
  },
  methods: {
    readFile: function(file) {
      var self = this;
      var paths = {};
      var path = file.webkitRelativePath;
      let ext = path.split('.')[1];
      var reader = new FileReader();

      // 読み込み完了時のイベント
      reader.onload = function(e) {
	var content = e.target.result;
	if(type === "text") {
	  content = window.btoa(unescape(encodeURIComponent(content)));
	}
	paths[path] = content;
	if(path.indexOf(".git") === -1) {
	  self.dir.push(paths);
	}
      };

      // テキストファイルかバイナリファイルか
      if(this.imgExts.indexOf(ext) >= 0) {
	var type = "binary";
	reader.readAsDataURL(file);
      } else {
	var type = "text";
	reader.readAsText(file);
      }
    },

    onDrop: function(event) {
      let files = event.target.files;
      for(let file of files) {
	this.readFile(file);
      }
    },

    compile: function() {
      var self = this;
      this.show = true;

      if(this.dir.length === 0) {
	this.show = false;
	alert("Select directory you want to upload.");
	return;
      }

      axios
	.post(urlBase + "/compile",
	      {files: this.dir}
	)
        .then(response => {
	  self.show = false;
	  window.open(response.data.url, '_blank');
	  location.reload();
	})
	.catch(error => {
	  self.show = false;
	  console.log(error);
	})
    },
  },
});

var app = new Vue({
	el: "#app",
	data: {
		imgFileList: [],
		processFileUrl: null,
		stepActiveNum: 0,
		activeTabName: "",
		dialogImageName: "",
		dialogImageUrl: "",
		dialogVisible: false,
	},
	methods: {
		TabClick(tab) {
			switch (tab.name) {
				case "1":
					this.stepActiveNum = 1;
					break;
				case "2":
					this.stepActiveNum = 2;
					break;
				case "3":
					this.stepActiveNum = 3;
					break;
			}
			if (tab.name == "2") {
				if (this.imgFileList.length == 0) {
					this.$message({
						showClose: true,
						message: "没有检测到图片上传",
						type: "error",
					});
				} else {
					var origincanvas = document.getElementById("origin");
					origincanvas.style.height = "300px";
					origincanvas.style.width = "250px";
					var ctx1 = origincanvas.getContext("2d");
					var img = new Image();

					img.onload = function () {
						let xRate = origincanvas.width / img.width;
						let yRate = origincanvas.height / img.height;

						ctx1.drawImage(this, 0, 0, img.width * xRate, img.height * yRate);
					};
					img.src = this.imgFileList[0].url;
				}
			}
		},
		RemovePicture(file, fileList) {
			// console.log(file, fileList);
			if ((file.url = this.processFileUrl)) {
				this.processFileUrl = null;
				var origincanvas = document.getElementById("origin");
				origincanvas.style.height = "0px";
				origincanvas.style.width = "0px";
				var procCanvas = document.getElementById("process");
				procCanvas.style.height = "0px";
				procCanvas.style.width = "0px";
			}
		},
		FileChange(file, fileList) {
			this.imgFileList = fileList;
		},
		PictureCardPreview(file) {
			this.dialogImageName = file.name;
			this.dialogImageUrl = file.url;
			this.dialogVisible = true;
		},
		NextStep() {
			// if (this.stepActiveNum++ > 2) this.stepActiveNum = 0;
		},
		ConfirmUpload() {
			if (this.imgFileList.length == 0) {
				this.$message({
					showClose: true,
					message: "没有检测到图片上传",
					type: "error",
				});
			} else {
				let param = new FormData();
				if (this.processFileUrl == null) {
					param.append(
						"file",
						this.dataURLtoFile(
							this.imgFileList[0].url,
							this.imgFileList[0].name
						)
					);
				} else {
					param.append(
						"file",
						this.base64ToFile(this.processFileUrl, this.imgFileList[0].name)
					);
				}

				// 注意添加headers
				axios
					.post("http://127.0.0.1:5000/file_upload", param, {
						headers: {
							"Content-Type": "multipart/form-data",
						},
					})
					.then((response) => {
						// console.log(response)
						if (response.data.code == "202") {
							this.$message({
								showClose: true,
								message: response.data.msg,
							});
						} else {
							this.$message({
								showClose: true,
								message: response.data.msg,
								type: "success",
							});

							let box = response.data.data.bbox;
							let confidence = response.data.data.confidence;
							let turbidity = response.data.data.turbidity;

							var rescanvas = document.getElementById("detected");
							rescanvas.style.height = "300px";
							rescanvas.style.width = "250px";
							var ctx = rescanvas.getContext("2d");
							var img = new Image();
							img.onload = function () {
								let xRate = rescanvas.width / img.width;
								let yRate = rescanvas.height / img.height;

								ctx.drawImage(
									this,
									0,
									0,
									img.width * xRate,
									img.height * yRate
								);

								ctx.font = "17px Arial";
								ctx.fillStyle = "#FF0000";
								ctx.fillText(
									"浊度值:" + turbidity,
									box[0] * xRate,
									box[1] * yRate
								);
								ctx.fillText("置信度:" + confidence, 20, 20);

								ctx.beginPath();
								ctx.lineWidth = "2"; //矩形线宽
								ctx.stokeStyle = "red"; //矩形线填充
								ctx.rect(
									box[0] * xRate,
									box[1] * yRate,
									(box[2] - box[0]) * xRate,
									(box[3] - box[1]) * yRate
								);
								ctx.stroke();
							};
							img.src = this.processFileUrl;
						}
					})
					.catch((error) => {
						// 处理错误情况
						console.log(error);
						this.$message({
							showClose: true,
							message: "图片上传服务器失败，请检查网络连接",
							type: "error",
						});
					})
					.then(() => {
						//总会执行
					});
			}
		},
		ImgCvt2Gray() {
			var procCanvas = document.getElementById("process");
			procCanvas.style.height = "300px";
			procCanvas.style.width = "250px";
			let src = cv.imread("origin");
			let dst = new cv.Mat();
			cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY, 0);
			cv.imshow("process", dst);
			this.processFileUrl = procCanvas.toDataURL("image/png");
			src.delete();
			dst.delete();
		},
		ImgMidFilter() {
			var procCanvas = document.getElementById("process");
			procCanvas.style.height = "300px";
			procCanvas.style.width = "250px";
			let src = cv.imread("origin");
			let dst = new cv.Mat();
			cv.medianBlur(src, dst, 5);
			cv.imshow("process", dst);
			this.processFileUrl = procCanvas.toDataURL("image/png");
			src.delete();
			dst.delete();
		},
		ImgGaussianFilter() {
			var procCanvas = document.getElementById("process");
			procCanvas.style.height = "300px";
			procCanvas.style.width = "250px";
			let src = cv.imread("origin");
			let dst = new cv.Mat();
			let ksize = new cv.Size(3, 3);
			cv.GaussianBlur(src, dst, ksize, 0, 0, cv.BORDER_DEFAULT);
			cv.imshow("process", dst);
			this.processFileUrl = procCanvas.toDataURL("image/png");
			src.delete();
			dst.delete();
		},
		ImgClearEffect(){
			var procCanvas = document.getElementById("process");
			procCanvas.style.height = "300px";
			procCanvas.style.width = "250px";
			let src = cv.imread("origin");
			cv.imshow("process", src);
			this.processFileUrl = procCanvas.toDataURL("image/png");
			src.delete();
		},
		base64ToFile: function (urlData, fileName) {
			let arr = urlData.split(",");
			let mime = arr[0].match(/:(.*?);/)[1];
			let bytes = atob(arr[1]);
			let n = bytes.length;
			let ia = new Uint8Array(n);
			while (n--) {
				ia[n] = bytes.charCodeAt(n);
			}
			return new File([ia], fileName, {
				type: mime,
			});
		},
		dataURLtoFile(dataurl, filename) {
			var arr = dataurl.split(","),
				mime = arr[0].match(/:(.*?);/)[1],
				bstr = atob(arr[1]),
				n = bstr.length,
				u8arr = new Uint8Array(n);
			while (n--) {
				u8arr[n] = bstr.charCodeAt(n);
			}
			return new File([u8arr], filename, {
				type: mime,
			});
		},
	},
});

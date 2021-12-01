<template>
<div>
  <div style="padding: 32px">
    <div style="
    height: 200px;
    display: flex;
    justify-content: space-between;
      ">
      <div style="flex: 1">
        <div style="
        color: rgb(32, 33, 36);
        font-size: 36px;
      line-height: 44px;
      font-weight: bold;
      font-family: zeitung, sans-serif;">
          镜像管理
        </div>

        <div style="
        margin-top: 20px;
    color: #808080;
    font-size: 14px;
    font-weight: 400;
    line-height: 22px;
    max-width: 485px;
    ">
          在这里管理您的镜像。镜像管理支持对镜像信息的创建与管理。
        </div>

        <el-button style="background-color: #333333;color: #FFFFFF;margin-top: 20px;" round @click="uploadDrawer=true;">+ 上传镜像</el-button>
        <el-button style="background-color: #333333;color: #FFFFFF;margin-top: 20px;" round @click="yamlManage"> yaml文件管理</el-button>
      </div>

      <div style="text-align: center;width: 200px;">

        <svg class="icon" aria-hidden="true" style="font-size: 200px">
          <use xlink:href="#icon-suanfa1"></use>
        </svg>

      </div>
    </div>

    <el-card>

      <div>
        <el-input v-model="searchInput" style="width:50%" placeholder="请输入内容"> </el-input>
        <svg class="icon" aria-hidden="true" style="font-size: 30px;margin-left: 20px;cursor: pointer" @click="searchImage">
          <use xlink:href="#icon-xingtaiduICON_sousuo--"></use>
        </svg>
      </div>


      <div >
        <el-table
            :data="tableData"
            stripe
            style="width: 100%">
          <el-table-column
              prop="name"
              label="镜像名称"
              width="200">
          </el-table-column>

          <el-table-column
              prop="version"
              label="镜像版本"
              width="180">
          </el-table-column>

          <el-table-column
              prop="tag"
              label="镜像标签"
              width="180">
          </el-table-column>

          <el-table-column
              prop="information"
              label="镜像信息"
              >
          </el-table-column>

          <el-table-column
              fixed="right"
              label="操作"
              width="300px">
            <template slot-scope="scope">

              <el-tooltip class="item" effect="dark" content="下载" placement="top">
                <svg class="icon" aria-hidden="true" style="margin-right:10px;font-size: 30px;cursor: pointer" @click="downloadImage(scope.row)">
                  <use xlink:href="#icon-xiazai2"></use>
                </svg>
              </el-tooltip>

              <el-tooltip class="item" effect="dark" content="删除" placement="top">
                  <svg class="icon" aria-hidden="true" style="margin-right:10px;font-size: 30px;cursor: pointer"  @click="isDeleteImage(scope.row)">
                    <use xlink:href="#icon-shanchu_"></use>
                  </svg>
              </el-tooltip>

              <el-button @click="createTask(scope.row)">训练任务</el-button>

            </template>
          </el-table-column>
        </el-table>

      </div>

    </el-card>

<!--    上传镜像-->
    <el-drawer
        title="上传镜像"
        :visible.sync="uploadDrawer"
        :before-close="handleClose"
        size='35%'
    >
      <div style="padding: 20px;color: #5D5D5D;height: 100%;position: relative">
        <div style="margin-bottom: 15px">
          <svg class="icon" aria-hidden="true" style="font-size: 20px">
            <use xlink:href="#icon-a-Calendar2"></use>
          </svg>
          镜像名称</div>
        <el-input style="margin-bottom: 20px" v-model="form.name" placeholder="请输入" ></el-input>


        <div style="margin-bottom: 15px">
          <svg class="icon" aria-hidden="true" style="font-size: 20px">
            <use xlink:href="#icon-a-Card4"></use>
          </svg> 镜像版本</div>
        <el-input style="margin-bottom: 20px" v-model="form.version" placeholder="请输入"></el-input>


        <div style="margin-bottom: 15px">
          <svg class="icon" aria-hidden="true" style="font-size: 20px">
            <use xlink:href="#icon-a-Card4"></use>
          </svg> 镜像信息</div>
        <el-input style="margin-bottom: 20px" v-model="form.information" placeholder="请输入"></el-input>


        <div style="margin-bottom: 15px">
          <svg class="icon" aria-hidden="true" style="font-size: 20px">
            <use xlink:href="#icon-a-Card4"></use>
          </svg> 镜像标签</div>
        <el-input style="margin-bottom: 20px" v-model="form.tag" placeholder="请输入"></el-input>


        <div style="margin-bottom: 15px">
          <svg class="icon" aria-hidden="true" style="font-size: 20px">
            <use xlink:href="#icon-a-Calendar5"></use>
          </svg> 上传镜像文件
          <el-upload
              class="upload-demo"
              ref="upload"
              :action="uploadUrl()"
              :http-request="httpRequest"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :file-list="fileList"
              :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
            <div slot="tip" class="el-upload__tip">只能上传压缩包</div>
          </el-upload>

        </div>


        <div style="position: absolute;left: 30px;bottom: 30px" @click="submitImage">
          <svg class="icon" aria-hidden="true" style="font-size: 30px;cursor: pointer">
            <use xlink:href="#icon-queding"></use>
          </svg>
        </div>

<!--        <el-button @click="testupload">测试上传</el-button>-->

      </div>

    </el-drawer>

<!--    yaml文件管理-->
    <el-drawer
        title="yaml 文件管理"
        :visible.sync="yamlDrawer"
        :before-close="handleClose"
        size='35%'
    >
      <div style="padding: 20px;color: #5D5D5D;height: 100%;position: relative">
        <el-button  round @click="uploadyaml"> 上传 yaml文件</el-button>

        <el-table
            :data="yamlTableData"
            style="width: 100%">
          <el-table-column
              prop="name"
              label="文件名称"
              width="400">
          </el-table-column>


          <el-table-column
              fixed="right"
              label="操作"
              >
            <template slot-scope="scope">

              <el-tooltip class="item" effect="dark" content="删除" placement="top">
                <svg class="icon" aria-hidden="true" style="margin-right:10px;font-size: 30px;cursor: pointer"  @click="deleteyaml(scope.row)">
                  <use xlink:href="#icon-shanchu_"></use>
                </svg>
              </el-tooltip>

            </template>

          </el-table-column>

        </el-table>

      </div>

    </el-drawer>


<!--    yaml文件上传-->
    <el-drawer
        title="上传yaml文件"
        :visible.sync="yamlUploadDrawer"
        :before-close="handleClose"
        size='35%'
    >
      <div style="padding: 20px;color: #5D5D5D;height: 100%;position: relative">
        <el-upload
            class="upload-demo"
            drag
            action="#"
            ref="uploadyaml"
            :file-list="yamlFileList"
            :on-change="yamlHandleChange"
            :http-request="submityaml"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">只能上传yaml文件</div>
        </el-upload>

      </div>

    </el-drawer>

<!--用于删除镜像对话框-->
    <el-dialog
        title="提示"
        :visible.sync="isDeleteImageDialogVisible"
        width="30%">
      <span>是否删除镜像</span>
      <span slot="footer" class="dialog-footer">
    <el-button @click="isDeleteImageDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="isDeleteImageConfirm">确 定</el-button>
  </span>
    </el-dialog>


<!--    <el-button @click="test">按钮</el-button>-->

  </div>
</div>
</template>

<script>

import axios from 'axios'
import request from "../utils/request";

export default {
  name: "ImageManage",
  data(){
    return{
      fileList:[],
      form:{
        name:"",
        version:"",
        information:"",
        tag:""
      },
      tableData:[
        {
          name: 'ddd',
          version: '王小虎',
        },{
          name: 'ddd',
          version: '王小虎',
        },
      ],
      searchInput:'',
      uploadDrawer:false,
      yamlDrawer:false,
      isDeleteImageDialogVisible:false,
      row:undefined,
      yamlTableData:[],
      yamlUploadDrawer:false,
      yamlFileList:[],


    }

  },
  created() {
    this.load();
  },


  methods: {
    yamlManage(){
      this.yamlDrawer=true;
      this.getAllyaml();
    },
    uploadyaml(){
      this.yamlUploadDrawer=true;
    },
    yamlHandleChange(file, fileList) {
      if(fileList.length>1){
        this.yamlFileList=fileList.slice(1);
      }
    },

    //上传yaml文件
    submityaml(){
      let file = this.$refs.uploadyaml.uploadFiles.pop().raw;//这里获取上传的文件对象
      let formData = new FormData();
      formData.append("file",file);
      request.post("api/uploadTrainConfig",formData).then(res=>{
        console.log(res);
        //上传成功
        if(res.code=="200"){
          this.yamlUploadDrawer=false;
          this.$message.success("上传成功");

          this.getAllyaml();
        }else{
          this.$message.error(res.msg);
        }
      });
    },

    //下载镜像
    downloadImage(row){
      request.post("api/pullImage",{imageName:row.name,imageVersion:row.version}).then(res=>{

        if(res.code=="200"){
          let link = document.createElement('a');
          //link.href = "flask/image/pullImage"+"?imageName="+row.name+"&imageVersion="+row.version;
          link.href=res.data;
          link.target = '_blank';
          link.style.display = 'none';
          document.body.appendChild(link);
          // 触发点击
          link.click();
          // 然后移除
          document.body.removeChild(link);
          link = null;
        }
      })

    },

    isDeleteImage(row){
      this.isDeleteImageDialogVisible=true;
      this.row=row;
    },
    isDeleteImageConfirm(){
      this.deleteImage(this.row);
      this.isDeleteImageDialogVisible=false;
    },
    //删除镜像
    deleteImage(row){
      request.post("api/deleteImage",{imageName:row.name,imageVersion:row.version}).then(res=>{

        if(res.code=="200"){
          this.$message({ type:"success", message:"删除镜像成功" });

          this.load();
        }else{
          this.$message({ type:"error", message:"删除失败" });
        }
      })

    },

    //删除yaml配置文件
    deleteyaml(row){
      console.log(row);
      request.post("api/deleteTrainConfig",{config_file_name:row.name}).then(res=>{

        if(res.code=="200"){
          this.$message.success("删除成功");
          this.getAllyaml();

        }else{
          this.$message.error("删除失败");

        }
      })


    },

    //加载页面
    load(){
      this.tableData=[];

      request.post("api/getAllImage").then(res=>{

        if(res.code=="200"){
          this.tableData=res.data;
        }
      })

    },
    //获取所有yaml文件
    getAllyaml(){
      request.get("api/getTrainConfigList").then(res=>{
        if(res.code=='200'){
          this.yamlTableData=[];
          for(let i=0;i<res.data.length;i++){
            let item={};
            let str=res.data[i];
            item['name']=str;
            this.yamlTableData.push(item);
          }
        }
      })

    },

    //搜索
    searchImage(){


      if(this.searchInput==""){
        this.load();
        return;
      }

      request.post("api/getImageByName",{name:this.searchInput}).then(res=>{

        if(res.code=='200'){
          this.tableData=res.data;
        }
      })


    },

    handleClose(done) {
      this.$confirm('确认关闭？')
          .then(_ => {
            this.form={}
            done();
          })
          .catch(_ => {});
    },
    submitUpload() {
      this.$refs.upload.submit();
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },

    uploadUrl:function(){
      return "http://172.16.20.190:15000/image/pushImage"+"?imageName="+this.form.name+"&imageVersion="+this.form.version;
    },

    //点击加号 提交镜像
    submitImage(){

      if(this.form.name!==""&&this.form.version!==""){
        this.submitUpload();
      }else{
        this.$message({ type:"error", message:"请填写完整" });
      }

    },

    httpRequest(param) {
      console.log(param);
      let fileObj = param.file // 相当于input里取得的files
      let fd = new FormData()// FormData 对象
      fd.append('file', fileObj)// 文件对象

      fd.append('imageName', this.form.name)
      fd.append('imageVersion', this.form.version)
      fd.append('tag', this.form.tag)
      fd.append('information', this.form.information)

      request.post('api/pushImage', fd).then(res=>{
        console.log(res);

        if(res.code=='200'){
          this.$message({ type:"success", message:"添加镜像成功" });
          this.form={};
          this.uploadDrawer=false;
          this.load();
        }else{
          this.$message({ type:"error", message:"添加失败" });
        }
      })

    },

    //同时请求多个接口的测试
    test(){

/*      request.post("api/getAllImage").then(res=>{
        console.log(res);
      })*/


      axios.all([axios.get("flask/image/getImageList").then(res => res.data),
        request.post("api/getAllImage").then(res=>res)
      ]).then(
          axios.spread((val1,val2) => {
            console.log('两个接口全部加载完成',val1,val2) ; // 1,2
          })
      )

/*      axios.post("api/getAllImage").then(res=>{
        console.log(res);
      })*/

    },

    //训练任务
    createTask(row){
      sessionStorage['name']=row.name;
      sessionStorage['version']=row.version;
      this.$router.push('uploadtask');
    }

  }

}
</script>

<style scoped>


</style>
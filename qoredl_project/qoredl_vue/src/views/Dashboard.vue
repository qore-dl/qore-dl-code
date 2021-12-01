<template>
  <div class="dashboard-editor-container">

    <el-row :gutter="40" class="panel-group">
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('newVisitis')">
          <div class="card-panel-icon-wrapper icon-people">

            <svg class="icon card-panel-icon" aria-hidden="false" >
              <use xlink:href="#icon-a-017-head"></use>
            </svg>

          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">
              Algorithms
            </div>
            <count-to :start-val="0" :end-val="102400" :duration="2600" class="card-panel-num" />
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('messages')">
          <div class="card-panel-icon-wrapper icon-message">

            <svg class="icon card-panel-icon" aria-hidden="false" >
              <use xlink:href="#icon-a-018-smartphone"></use>
            </svg>

          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">
              Models
            </div>
            <count-to :start-val="0" :end-val="81212" :duration="3000" class="card-panel-num" />
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('purchases')">
          <div class="card-panel-icon-wrapper icon-money">

            <svg class="icon card-panel-icon" aria-hidden="false" >
              <use xlink:href="#icon-a-014-settings-1"></use>
            </svg>

          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">
              tests
            </div>
            <count-to :start-val="0" :end-val="9280" :duration="3200" class="card-panel-num" />
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('shoppings')">
          <div class="card-panel-icon-wrapper icon-shopping">

            <svg class="icon card-panel-icon" aria-hidden="false" >
              <use xlink:href="#icon-a-016-file-3"></use>
            </svg>

          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">
              data
            </div>
            <count-to :start-val="0" :end-val="13600" :duration="3600" class="card-panel-num" />
          </div>
        </div>
      </el-col>
    </el-row>

  </div>
</template>

<script>
import CountTo from 'vue-count-to'

export default {
  name: "Dashboard",
  components: {
    CountTo
  },

}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
}
.card-panel-col {
  margin-bottom: 32px;
}

.card-panel {
  height: 108px;
  cursor: pointer;
  font-size: 12px;
  position: relative;
  overflow: hidden;
  color: #666;
  background: #fff;
  box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
  border-color: rgba(0, 0, 0, .05);

  .card-panel-icon-wrapper {
    float: left;
    margin: 14px 0 0 14px;
    padding: 16px;
    transition: all 0.38s ease-out;
    border-radius: 6px;
  }

  .card-panel-icon {
    float: left;
    font-size: 48px;
  }

  .card-panel-description {
    float: right;
    font-weight: bold;
    margin: 26px;
    margin-left: 0px;

    .card-panel-text {
      line-height: 18px;
      color: rgba(0, 0, 0, 0.45);
      font-size: 16px;
      margin-bottom: 12px;
    }

    .card-panel-num {
      font-size: 20px;
    }
  }

}




</style>
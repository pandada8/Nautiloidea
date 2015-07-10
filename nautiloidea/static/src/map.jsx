import {ak} from "./config";
import React from "react";

console.log(ak)

class BaiduMap extends React.Component {
    constructor(props){
        super(props)
        if(window.BMAP){
            this.state = {loaded: true}
        }else{
            this.state = {loaded: false}
            this.loadScript(() => {
                this.setState({loaded: true})
                setTimeout(() => {
                    this.init_maps()
                }, 10)
            })
        }
    }
    loadScript(cb){
        var script = document.createElement('script')
        script.type = "text/javascript";
        script.src  = `http://api.map.baidu.com/getscript?v=1.5&ak=${ak}&services=`;
        script.onload = cb ? cb : null;
        document.body.appendChild(script)
    }
    init_maps (){
        var dom = React.findDOMNode(this.refs.target)
        var map = this.state.map = new BMap.Map(dom)
        map.enableScrollWheelZoom()
        map.disableDragging()
        map.enableKeyboard()
        if (this.props.position){
            var center = new BMap.Point(this.props.position.longitude, this.props.position.latitude);
            map.centerAndZoom(center, 15);
        }
    }
    render(){
        var style = {
            "height": '200px',
            "width": "100%"
        }
        var target_style = {height: "100%"};
        if(this.state.loaded){
            return <div className="ui segment" style={style}>
                <div className="" style={target_style} ref="target"></div>
            </div>
        }else if (this.props.position){
            return <div className="ui segment" style={style}>
                <div className="ui active inverted dimmer">
                    <div className="ui text loader">载入地图组件</div>
                </div>
            </div>
        }else{
            return <div className="ui segment" style={style}>
                <div className="ui active inverted dimmer">
                    <div>没有位置信息</div>
                </div>
            </div>
        }
    }
}

export default BaiduMap;

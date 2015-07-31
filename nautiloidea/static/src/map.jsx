import {ak} from "./config.jsx";
import React from "react";

class BaiduMap extends React.Component {
    componentDidMount(){
        if(!window.BMap){
            this.loadScript(() => {
                this.forceUpdate()
                setTimeout(() => {
                    this.init_maps()
                }, 10)
            })
        }else{
            setTimeout(() => {
                console.log(this.props)
                this.init_maps()
            }, 10)
        }
    }
    loadScript(cb){
        var script = document.createElement('script')
        script.type = "text/javascript";
        script.src  = `http://api.map.baidu.com/getscript?v=1.5&ak=${ak}&services=`;
        script.onload = cb ? cb : null;
        document.body.appendChild(script)
    }
    update(position){
        if(this.map){
            console.log(position.longtitude, position.latitude)
            var center = new BMap.Point(position.longtitude, position.latitude);
            var marker = new BMap.Marker(center);
            this.map.clearOverlays();
            if(this.inited){
                this.map.panTo(center);
            }else{
                this.map.centerAndZoom(center, 15);
            }
            this.map.addOverlay(marker);
        }else{
            this.props.position = position;
        }
    }
    init_maps (){
        var dom = React.findDOMNode(this.refs.target)
        var map = this.map = new BMap.Map(dom)
        map.enableScrollWheelZoom()
        map.enableKeyboard()
        if (this.props.position){
            this.update(this.props.position)
            this.inited = true;
        }
    }
    render(){
        var style = {
            "height": '300px',
            "width": "100%"
        }
        var target_style = {height: "100%"};
        console.log(this.props)

        if(window.BMap){
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
                <div className="ui inverted active dimmer">
                    <div className="ui text loader">没有位置信息</div>
                </div>
            </div>
        }
    }
}

export default BaiduMap;

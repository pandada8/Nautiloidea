import {ak} from "./config.jsx";
import React from "react";

class BaiduMap extends React.Component {
    constructor(props){
        super(props)
        this.state = {position: this.props.position}
    }
    componentDidMount(){
        if(!window.BMAP){
            this.loadScript(() => {
                this.forceUpdate()
                setTimeout(() => {
                    if (this.state.position){
                        this.init_maps()
                    }
                }, 10)
            })
        }else{
            if (this.state.position){
                this.forceUpdate()
                this.init_maps()
            }
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
        map.enableKeyboard()
        if (this.props.position){
            var center = new BMap.Point(this.props.position.longitude, this.props.position.latitude);
            var marker = new BMap.Marker(center);
            map.centerAndZoom(center, 15);
            map.addOverlay(marker);
        }
    }
    update_position(longitude, latitude){

    }
    render(){
        var style = {
            "height": '300px',
            "width": "100%"
        }
        var target_style = {height: "100%"};
        console.log(this.props.position)
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
                <div className="ui inverted active dimmer">
                    <div className="ui text loader">没有位置信息</div>
                </div>
            </div>
        }
    }
}

export default BaiduMap;

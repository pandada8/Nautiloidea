import React from "react";
import { Router, Route } from 'react-router';
import moment from "moment";
import _ from "moment/locale/zh-cn.js"

class Menu extends React.Component {
    render() {
        var {username} = this.props.data
        return <div className="ui menu">
            <div className="right menu">
                <span className="item">
                    {username}
                </span>
                <a href="/logout" className="item">
                    <i className="red sign out icon"></i>退出登录
                </a>
            </div>
        </div>
    }
 }

class Phone extends React.Component {
    render() {
        var {phone_number, last_status: { time, status }} = this.props.device;
        return <div className="ui card">
            <div className="image">
            	<i className="green check circle icon"></i>
            	<p className="ui centered header">{phone_number}</p>
            </div>
            <div className="content">
            	<p>上次通信：{new Date(time).toLocaleString()}</p>
            	<p>现在状态：{status}</p>
            </div>
        </div>
    }
}

class App  extends React.Component {
    constructor(props){
        super(props);
        this.state = {data: data};
    }
    render() {
        var {devices} = this.state.data;
        return <div className="ui stackable grid container" style={{paddingTop: 3+"rem"}} id="app">
            <div className="sixteen wide column">
                <Menu data={this.state.data} />
            </div>
            <div className="four columns" id="phones">
                {devices.map(function(device){
                    return <Phone device={device} />
                })}
            </div>
		</div>
    }
}

React.render(
    <App />,
    document.getElementById('app')
);

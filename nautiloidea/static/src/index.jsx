import React from "react";
import { Router, Route, Link, Redirect } from 'react-router';
import { history } from 'react-router/lib/HashHistory';
import moment from "moment";
import _ from "moment/locale/zh-cn.js"

class Menu extends React.Component {
    render() {
        var {username} = this.props.data,
            devices_number = this.props.data.devices.length
        return <div className="ui menu">
            <span className="item">{devices_number}台设备</span>
            <div className="right menu">
                <span className="item">
                    <i className="user icon"></i>{username}
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
        var {phone_number, last_status: { time, event }} = this.props.device,
            now = Date.now(),
            status = '未知';

        if(time && event){
            if(event != 'offline'){
                if(now - time > 60 * 1000){
                    status = '离线'
                }else{
                    status = '在线'
                }
            }else{
                status = '离线'
            }
        }
        time = time === undefined ? "未知" : new Date(time).toLocaleString()
        var icon = {'未知':'minus circle', '离线': "red remove circle", '在线': "green check circle"}[status] + ' icon status';
        var phone_url = "phone/" + this.props.device.id;

        return <Link className="ui card" to={phone_url}>
            <div className="image">
            	<i className={icon}></i>
                <p className="ui centered header status-text">{status}</p>
            	<p className="ui centered header">{phone_number}</p>
            </div>
            <div className="content">
            	<p>上次通信：{time}</p>
            </div>
        </Link>
    }
}

class IndexPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {data: data};
    }
    render() {
        var {devices} = this.state.data;
        return <div className="ui link cards" id="phones">
                {devices.map(function(device){
                    return <Phone device={device} />
                })}
            </div>

    }
}

class App extends React.Component {
    constructor(props){
        super(props);
        this.state = {data: data};
    }
    render(){
        var {devices} = this.state.data;
        return <div className="ui stackable grid container" style={{paddingTop: 3+"rem"}} id="app">
            <div className="sixteen wide column">
                <Menu data={this.state.data} />
            </div>
            {this.props.children}
		</div>
    }
}

var PhonePage = React.createClass({
    render(){
        return <h1>Test</h1>
    }
})

React.render(
    <Router history={history}>
        <Route component={App}>
            <Route path="/" component={IndexPage} />
            <Route path="phone/:phone_id" component={PhonePage} />
        </Route>
     </Router>, document.getElementById('app')
)

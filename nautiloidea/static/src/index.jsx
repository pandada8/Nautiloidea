import React from "react";
import { Router, Route, Link, Redirect } from 'react-router';
import { history } from 'react-router/lib/HashHistory';
import BaiduMap from "./map";
import request from "superagent";


class Menu extends React.Component {
    render() {
        var {username} = this.props.data,
            devices_number = this.props.data.devices.length
        return <div className="ui menu">
            <Link to="/" className="item">{devices_number}台设备</Link>
            <Link to="/bind_guide" className="item">绑定设备</Link>
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
        console.log(this.props.device)
        var {deviceName, last_status} = this.props.device,
            time = last_status.status ? last_status.status.time * 1000 : null,
            event = last_status.status ? last_status.status.event : null,
            now = Date.now(),
            status = '未知';
        console.log(time, event, now)
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
        var icon = {'未知':'minus circle', '离线': "red remove circle", '在线': "green check circle"}[status] + ' icon status';
        var phone_url = "phone/" + this.props.device.deviceid;
        var ui_fix = {marginTop: '30px !important'};
        return <Link className="ui card" to={phone_url} style={ui_fix}>
            <div className="image">
            	<i className={icon}></i>
                <p className="ui centered header status-text">{status}</p>
            	<p className="ui centered header">{deviceName}</p>
            </div>
            <div className="content">
            	<p>上次通信：{time === null ? "未知" : new Date(time).toLocaleString()}</p>
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

class PhonePage extends React.Component{
    constructor(props){
        super(props)
        this.state = {messages: [], last_status: {}, init_position: {}}
        this.deviceid = this.props.params.phone_id
    }
    update(cb){
        request.get('/status')
                .query({device: this.deviceid})
                .end((err, resp)=>{
                    if(err){
                        console.error(err)
                    }else{
                        if(resp.err){
                            console.log(err)
                        }else{
                            cb(resp.body.status)
                        }
                    }
                })
    }
    componentWillMount(){
        this.update((status) => {
            this.setState({last_status: status, init_position: status.position, files: status.files})
        })
        this.timer = setInterval(()=>{
            this.update((status) => {
                if (status.files.time > this.state.files.time){
                    // the files is updated
                    this.setState({files_update: true})
                }
                this.setState({last_status: status, files: status.files})
                this.refs.map.update(status.position)
            })
        }, 2000)
    }
    erase(){
        var eraseNode = React.findDOMNode(this.refs.erase)
        eraseNode.className += ' loading'
        var data = {operation: "erase"}
        this.sendRequests(data, ()=>{
            eraseNode.className = eraseNode.className.replace("loading", '')
            this.alert("擦除手机请求发送成功")
        })
    }
    alarm(){
        var alarm = React.findDOMNode(this.refs.alarm)
        alarm.className += ' loading'
        var data = {operation: "alarm"}
        this.sendRequests(data, (err, response)=>{
            alarm.className = alarm.className.replace("loading", '')
            if(!err && !response.err){
                this.alert("响铃请求发送成功")
            }else{
                this.alert('Oops, 服务器出了一些问题')
            }

        })
    }
    unlock(){
        var alarm = React.findDOMNode(this.refs.unlock)
        alarm.className += ' loading'
        var data = {operation: "unlock"}
        this.sendRequests(data, (err, response)=>{
            alarm.className = alarm.className.replace("loading", '')
            if(!err && !response.err){
                this.alert("解锁请求发送成功")
            }else{
                this.alert('Oops, 服务器出了一些问题')
            }

        })
    }
    disalarm(){
        var alarm = React.findDOMNode(this.refs.disalarm)
        alarm.className += ' loading'
        var data = {operation: "disalarm"}
        this.sendRequests(data, (err, response)=>{
            alarm.className = alarm.className.replace("loading", '')
            if(!err && !response.err){
                this.alert("取消响铃请求发送成功")
            }else{
                this.alert('Oops, 服务器出了一些问题')
            }

        })
    }
    sendRequests(data, cb){
        request.post('/operation')
            .type('form')
            .send(data)
            .send({deviceid: this.deviceid})
            .end(cb)
    }
    alert(msg){
        this.setState({messages: [msg].concat(this.state.messages)})
        setTimeout(()=>{
            this.setState({messages: this.state.messages.slice(0, -1) })
        }, 3000)
    }
    lock(){
        var alarm = React.findDOMNode(this.refs.lock)
        alarm.className += ' loading'
        var data = {operation: "lock"}
        this.sendRequests(data, (err, response)=>{
            alarm.className = alarm.className.replace("loading", '')
            if(!err && !response.err){
                this.alert("锁定请求发送成功")
            }else{
                this.alert('Oops, 服务器出了一些问题')
            }

        })
    }
    getFile(){

    }
    componentWillUnmount(){
        // delete the timer
        clearInterval(this.timer)
    }
    render(){
        // TODO: Using data
        var time = this.state.last_status.position ? new Date(this.state.last_status.position.t).toLocaleString() : "未知";
        if(this.state.files && this.state.files.data){
            // we got some data
            var getFileBtn = <div className="ui yellow button" onClick={this.getFile.bind(this)} ref="getFile">获取文件</div>
        }else{
            var getFileBtn = "";
        }
        var unlock_btn = <div className="ui yellow button" onClick={this.getFile.bind(this)} ref="getFile">刷新文件列表</div>
        return <div className="sixteen wide column">
            <BaiduMap position={this.state.init_position} ref="map"/>
            <span>{}</span>
            <div className="ui segments">
                <div className="ui segment">
                    <p>操作</p>
                </div>
                <div className="ui secondary segment">
                    <div className="ui red button" onClick={this.erase.bind(this)} ref="erase">擦除手机</div>
                    <div className="ui yellow button" onClick={this.alarm.bind(this)} ref="alarm">响铃</div>
                    <div className="ui yellow button" onClick={this.lock.bind(this)} ref="lock">锁定手机</div>
                    <div className="ui yellow button" onClick={this.unlock.bind(this)} ref="unlock">解锁手机</div>
                    <div className="ui yellow button" onClick={this.disalarm.bind(this)} ref="disalarm">取消响铃</div>
                    <div className="ui yellow button" onClick={this.getFile.bind(this)} ref="getFile">获取文件</div>
                </div>
            </div>
            <div className="ui messages">
                {this.state.messages.map((x) => {
                    return <div className="ui message"><i className="notched circle loading icon"></i>{x}</div>
                })}
            </div>
        </div>
    }
}

class BindGuidePage extends React.Component{
    render(){
        return <div className="sixteen wide column">
            <div className="ui segment">
                <h2 className="header">怎样绑定我的手机？</h2>
                <p>点击<a href="#" target="_blank">链接</a>下载应用，安装登陆后根据说明操作。</p>
            </div>
        </div>
    }
}

class PhoneGetFile extends React.Component {
    // directly build thefile tree ignore the performnace issue
    getFile(){
        request.get('/status')
                .query({device: this.deviceid})
                .end((err, resp)=>{
                    if(err){
                        console.error(err)
                    }else{
                        if(resp.err){
                            console.log(err)
                        }else{
                            cb(resp.body.status)
                        }
                    }
                })
    }
    render(){
        return <div className="sixteen wide column">
            <div className="ui segment">
            </div>
        </div>
    }
}

React.render(
    <Router history={history}>
        <Route component={App}>
            <Route path="/" component={IndexPage} />
            <Route path="phone/:phone_id" component={PhonePage} />
            <Route path="phone/:phone_id/files" component={PhoneGetFile} />
            <Route path="bind_guide" component={BindGuidePage} />
        </Route>
     </Router>, document.getElementById('app')
)

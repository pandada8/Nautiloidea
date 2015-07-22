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
        // console.log(this.props.device)
        var {deviceName, last_status} = this.props.device,
            time = last_status.status ? last_status.status.time * 1000 : null,
            event = last_status.status ? last_status.status.event : null,
            now = Date.now(),
            status = '未知';
        // console.log(time, event, now)
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



class FileList extends React.Component{
    constructor(props){
        super(props)
        this.state = {list: {}, finished: [], path: undefined}
    }
    update(files, finished){
        // console.log(files, finished);
        var state = {list: files, finished: finished}
        if(!this.state.path){
            state.path = files.data.path
        }
        this.setState(state)
    }
    find_file_for_path(path, tree){
        if(tree.path == path){
            return tree.items
        }else{
            for (var i in tree.items){
                var new_root = tree.items[i]
                if (new_root.isFolder){
                    var result = this.find_file_for_path(path, new_root);
                    if (result){
                        return result
                    }
                }
            }
        }
    }
    download(x){
        var loader =  React.findDOMNode(this.refs.loader)
        loader.className += " active"
        if(!x.isFolder){
            this.props.download(x.path, ()=>{
                loader.className = loader.className.replace(' active', '')
            })
        }else{
            console.log('Jump to new path', x.path);
            this.setState({path: x.path})
            loader.className = loader.className.replace(' active', '')
        }
    }
    up(){
        if(this.state.path != this.state.list.data.path){
            var newpath = this.state.path.split('/').slice(0, -1).join('/')
            this.setState({path: newpath})
            console.log('New Path', newpath);
        }
    }
    render(){
        console.log(this.state.path);
        if(this.state.list.data){
            var files = this.find_file_for_path(this.state.path, this.state.list.data)
            console.log(files);
        }else{
            var files = []
        }
        return <div className="ui segment">
            <div className="ui inverted dimmer" ref="loader">
                <div className="ui text loader">Loading</div>
            </div>
            <div className="ui two column">
                <div className="column">
                    <p>{this.state.path}</p>
                    <div className="ui list">
                        <div className='item' onClick={this.up.bind(this)}>向上</div>
                        {files.map((x) => {
                            var icon = "ui " + (x.isFolder? 'folder' : 'file') + " icon"
                            return <div className="item" onClick={this.download.bind(this, x)}>
                                <i className={icon}></i>
                                <div className="content">
                                    {x.path.split('/').slice(-1)[0]}
                                </div>
                            </div>
                        })}
                    </div>
                </div>
                <div className="column">
                    <p className="head">完成的文件</p>
                    <div className="ui list">
                        {this.state.finished.map((x) => {
                            return <div className="item">
                                <div className="content">
                                    <a href={"/f/"+x.file_id}>{x.origin_path}</a>
                                </div>
                            </div>
                        })}
                    </div>
                </div>
            </div>

        </div>
    }
}

class PhonePage extends React.Component{
    constructor(props){
        super(props)
        this.state = {messages: [], last_status: {}, init_position: {}, files: {}}
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
                            cb(resp.body.status, resp.body.files, resp.body.uploaded)
                        }
                    }
                })
    }
    componentWillMount(){
        this.update((status, files, finished) => {
            this.setState({last_status: status, init_position: status.position, files: files})
        })
        this.timer = setInterval(()=>{
            this.update((status, files, finished) => {
                console.log(this.refs.files)
                if (files.time > this.state.files.time){
                    // the files is updated
                    this.alert("有新的文件数据！")
                }
                this.setState({last_status: status, files: files})
                this.refs.files.update(files, finished);
                this.refs.map.update(status.position);
            })
        }, 5000)
    }
    erase(){
        var eraseNode = React.findDOMNode(this.refs.erase)
        eraseNode.className += ' loading'
        var data = {operation: "erase"};
        var password = "我们需要您的密码来验证您的身份";
        data['password'] = password;
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
        var password = "我们需要您的密码来验证您的身份";
        data['password'] = password;
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
    getFile(path){
        var alarm = React.findDOMNode(this.refs.getFileList)
        alarm.className += ' loading'
        var data = {operation: "get_list"}
        this.sendRequests(data, (err, response)=>{
            alarm.className = alarm.className.replace("loading", '')
            if(!err && !response.err){
                this.alert("获取文件列表请求发送成功")
            }else{
                this.alert('Oops, 服务器出了一些问题')
            }
        })
    }
    componentWillUnmount(){
        // delete the timer
        clearInterval(this.timer)
    }
    download(path, cb){
        var data = {operation: "get_file", 'path': path}
        this.sendRequests(data, (err, response)=>{
            if(!err && !response.err){
                this.alert("上载文件请求发送成功")
            }else{
                this.alert('Oops, 服务器出了一些问题')
            }
            cb()
        })
    }
    render(){
        // TODO: Using data
        var time = this.state.last_status.position ? new Date(this.state.last_status.position.t).toLocaleString() : "未知";
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
                    <div className="ui yellow button" onClick={this.getFile.bind(this)} ref="getFileList">刷新文件列表</div>
                </div>
            </div>
            <div className="ui messages">
                {this.state.messages.map((x) => {
                    return <div className="ui message"><i className="notched circle loading icon"></i>{x}</div>
                })}
            </div>
            <FileList download={this.download.bind(this)} ref="files"></FileList>
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

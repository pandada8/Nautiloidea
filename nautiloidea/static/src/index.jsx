import React from "react";
// import { Router, Route } from 'react-router';
// import { history } from 'react-router/lib/BrowserHistory';

var Menu = React.createClass({
    render() {
        return <div className="ui menu">
            <div className="right menu">
                <span className="item">
                    {this.props.user.username}
                </span>
                <a href="/logout" className="item">
                    <i className="red sign out icon"></i>退出登录
                </a>
            </div>
        </div>
    }
})

class Card extends React.Component {
    render(phone) {
        return <div className="ui card">
            <div className="image">
            	<i className="green check circle icon"></i>
            	<p className="ui centered header">这里是手机的名字</p>
            </div>
            <div className="content">
            	<p>上次通信：[date]</p>
            	<p>现在状态：【state】</p>
            </div>
        </div>
    }
}

React.render(
    <Menu user={data} />,
    document.getElementById('menu')
);

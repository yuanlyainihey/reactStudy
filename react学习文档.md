## react 安装

1. 安装node.js

2. 通过npm使用react

   ```git
   $ npm install -g cnpm --registry=https://registry.npm.taobao.org
   $ npm config set registry https://registry.npm.taobao.org
   ```

3. 使用create-react-app快速构建React开发环境

   ```git
   $ cnpm install -g create-react-app
   $ create-react-app my-app
   $ cd my-app/
   $ npm start
   ```

   注：开发中使用yarn管理包

## react 元素渲染

```react
// 计时器举例 -- 1：创建新元素后渲染
function tick(){
    const element = (
    	<div>
        	<h1>时间：{new Date().toLocaleTimeString() }</h1>
        </div>
    );
    ReactDom.render(
    	element,
        document.getElementById('example')
    );
}
setInterval(tick, 1000);
// 计时器举例 -- 2：函数封装
function Clock(props){
    return(
        <div>
        	<h1>时间：{props.date.toLocaleTimeString() }</h1>
        </div>
    );
}
function tick(){
    ReactDom.render(
    	<Clock date={ new Date() } />,
        document.getElementById('example')
    );
}
setInterval(tick, 1000);
// 计时器举例 -- 3：React.Component的ES6类
class Clock extends React.Component{
    render(){
        return{
            <div>
                <h1>时间：{ this.props.date.toLocaleTimeString() }</h1>
            </div>
        };
    }
}
function tick(){
    ReactDom.render(
    	<Clock date={ new Date() } />,
        document.getElementById('example')
    );
}
setInterval(tick, 1000);
```

## react JSX

```react
// myDivElement可以是一个或多个HTML标签，在嵌套多个时需要用div元素包裹
var myStyle = { fontSize: 100, color: '#FF0000' };
var arr = [<h1>标题1</h1>, <h2>标题2</h2>];
var myDivElement = <div className="clsn" />;	// 一个HTML标签
				 = <h1>...</h1>;				// 一个HTML标签
				 = <div>
                       <h1 style = { myStyle }>...</h1>		  // 样式
                       <h1>{...}</h1>						  // 表达式
                       {/*...注释...*/}						 // 注释
                       <div>{arr}</div>						  // 数组
                   </div>						// 嵌套多个HTML标签
ReactDom.render(
	myDivElement,
	document.getElementById('example')
);
```

## react 组件

```react
// 定义组件方式 -- 1：函数
function func(props){
    return <h1>{ props.msg }</h1>;
}
// 定义组件方式 -- 2：ES6 class
class func extends React.Component{
    render(){
        return <h1>{ props.msg }</h1>;
    }
}
// 单组件举例
const element = <func msg="parameter" />
ReactDom.render(
	element,
    document.getElementById('example')
);
// 复合组件举例
function Name(props) {
    return <h1>网站名称：{ props.name }</h1>;
}
function Url(props) {
    return <h1>网站地址：{ props.url }</h1>;
}
function Nickname(props) {
    return <h1>网站昵称：{ props.nickname }</h1>;
}
function App() {
    return (
        <div>
            <Name name="web name" />
            <Url url="web url" />
            <Nickname nickname="web nickname" />
        </div>
    );
}
ReactDOM.render(
     <App />,
    document.getElementById('example')
);
```

## react State(状态)

> 状态通常被称为**局部或封装**。 除了拥有并设置它的组件外，其它组件不可访问。
>
> 通常被称为**自顶向下或单向数据流**。 任何状态始终由某些特定组件所有，并且从该状态导出的任何数据或 UI 只能影响树中下方的组件。
>
> 在 React 应用程序中，组件是有状态还是无状态被认为是可能随时间而变化的组件的实现细节。

```react
// FormattedDate组件将在其属性中接收到 date 值，并且不知道它是来自 Clock 状态、还是来自 Clock 的属性、亦或手工输入
function FormattedDate(props){
    return <h1>时间：{ props.date.toLocaleTimeString() }</h1>;
}
class Clock extends React.Component{
    // 类构造函数初始化状态 this.state
    // 类组件使用props调用基础构造函数
    constructor(props){
        super(props);
        this.state = { date: new Date() };
    }
    // componentDidMount() & componentWillUnmount()：生命周期钩子
    // Clock组件挂载：Clock组件第一次加载至DOM时生成定时器
    componentDidMount(){
        this.timerID = setInterval( ()=>this.tick(), 1000);
        // ()=>this.tick()		箭头函数表达式，ES6 中声明函数的一种方式
        // 引入箭头函数有两个方面的作用：更简短的函数并且不绑定 this
    }
    // Clock组件卸载：Clock生成的DOM被移除时清除定时器
    componentWillUnmount(){
        clearInterval(this.timerID);
    }
    tick(){
        this.setState({ date: new Date() });
    }
    // render()方法中使用 this.state 修改当前时间
    render(){
        return (
        	<div>
            	<h1>时间：{ this.state.date.toLocaleTimeString() }</h1>
                <FormateedDate date={ this.state.date } />
            </div>
        );
    }
}
ReactDom.render(
	<Clock />,
    document.getElementById('example')
)
```

**代码执行顺序**

> 1. 当 <Clock /> 被传递给 ReactDOM.render() 时，React 调用 Clock 组件的构造函数。 由于 Clock 需要显示当前时间，所以使用包含当前时间的对象来初始化 this.state 。我们稍后会更新此状态。
> 2. React 然后调用 Clock 组件的 render() 方法。这是 React 了解屏幕上应该显示什么内容，然后 React 更新 DOM 以匹配 Clock 的渲染输出。
> 3. 当 Clock 的输出插入到 DOM 中时，React 调用 componentDidMount() 生命周期钩子。 在其中，Clock 组件要求浏览器设置一个定时器，每秒钟调用一次 tick()。
> 4. 浏览器每秒钟调用 tick() 方法。 在其中，Clock 组件通过使用包含当前时间的对象调用setState() 来调度UI更新。 通过调用 setState() ，React 知道状态已经改变，并再次调用render() 方法来确定屏幕上应当显示什么。 这一次，render() 方法中的 this.state.date 将不同，所以渲染输出将包含更新的时间，并相应地更新 DOM。
> 5. 一旦 Clock 组件被从 DOM 中移除，React 会调用 componentWillUnmount() 这个钩子函数，定时器也就会被清除。

```react
## 下列两种函数定义等价
var f = ([参数]) => 表达式（单一）
var f = function([参数]){ return 表达式; }

## 箭头函数的基本语法
1. (参数1, 参数2, …, 参数N) => { 函数声明 }
2. (参数1, 参数2, …, 参数N) => 表达式（单一）
   (参数1, 参数2, …, 参数N) => { return 表达式; }
// 当只有一个参数时，圆括号是可选的
(单一参数) => { 函数声明 }
单一参数 => { 函数声明 }
// 没有参数的函数应该写成一对圆括号
() => { 函数声明 }
```

## React Props

> state 和 props 主要的区别： **props 是不可变的**，state 可以根据与用户交互来改变。
>
> 因此有些容器组件需要定义 state 来更新和修改数据。而子组件只能通过 props 传递数据。

```react
class func extends React.Component{
    render(){
        return (
        	<h1>指定props参数：{ this.props.parameter }</h1>
        );
    }
}
// 非默认 Props
const element = <func parameter='parameter' />
// 通过组件类的 defaultProps 属性为 props 设置默认值
func.defaultProps = { parameter: 'parameter' };
const element = <func />;

ReactDom.render(
	element,
    document.getElementById('example')
);
```

**State和Props的组合使用**

> 在父组件中设置 state， 并通过在子组件上使用 props 将其传递到子组件上。
>
> 在 render 函数中,设置 name 和 site 来获取父组件传递过来的数据。

```react
class Name extends React.Component{
    render(){
        return (
        	<h1>{ this.props.name }</h1>
        );
    }
}
class Link extends React.Component{
    render(){
        return (
            <a href={ this.props.site }>{ this.props.site }</a>
        );
    }
}
class WebSite extends React.Component{
    constructor(){
        super();
        this.state = {
            name: 'name-msg',
            site: 'site-msg'
        }
    }
    render(){
        return (
        	<div>
            	<Name name={ this.state.name } />
                <Link site={ this.state.site } />
            </div>
        );
    }
}
ReactDom.render(
	<WebSite />,
    document.getElementById('example')
);
```

**Props 验证**

> Props 验证使用 **propTypes**，它可以保证我们的应用组件被正确使用。
>
> React.PropTypes 提供很多验证器 (validator) 来验证传入数据是否有效。
>
> 当向 props 传入无效数据时，JavaScript 控制台会抛出警告。
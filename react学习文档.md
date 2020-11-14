## git 操作

```git
git init
git pull
git add ./*
git commit -m "xxxx"
git push -u origin master
```
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
> **React.PropTypes** 提供很多验证器 (validator) 来验证传入数据是否有效。
>
> 当向 props 传入无效数据时，JavaScript 控制台会抛出警告。

```react
var title = 'title';
## 方法 - 1
class MyTitle extends React.Component {
  render() {
    return (
      <h1>{ this.props.title }</h1>
    );
  }
}
// 数据类型验证
MyTitle.propTypes = {
  title: PropTypes.string
};
## 方法 - 2
var myTitle = React.createClass({
    propTypes: {
        title: React.PropTypes.string.isRequired
    },
    render: function(){
        return <h1>{ this.props.title }</h1>;
    }
});

ReactDOM.render(
    <MyTitle title={ title } />,
    document.getElementById('example')
);
```

**更多验证器说明**

```react
MyComponent.propTypes = {
    // 可以声明 prop 为指定的 JS 基本数据类型，默认情况，这些数据是可选
    optionalArray: React.PropTypes.array,
    optionalBool: React.PropTypes.bool,
    optionalFunc: React.PropTypes.func,
    optionalNumber: React.PropTypes.number,
    optionalObject: React.PropTypes.object,
    optionalString: React.PropTypes.string,
    
    // 可以被渲染的对象：numbers, strings, elements, array
    optionalNode: React.PropTypes.node,
    
    // React 元素
    optionalElement: React.PropTypes.element,
    
    // 用 JS 的 instanceof 操作符声明 prop 为类的实例。
    optionalMessage: React.PropTypes.instanceOf(Message),
    
    // 用 enum 来限制 prop 只接受指定的值。
    optionalEnum: React.PropTypes.oneOf(['News', 'Photos']),
    
    // 可以是多个对象类型中的一个
    optionalUnion: React.PropTypes.oneOfType([
        React.PropTypes.string,
        React.PropTypes.number,
        React.PropTypes.instanceOf(Message)
    ]),
    // 指定类型组成的数组
    optionalArrayOf: React.PropTypes.arrayOf(React.PropTypes.number),
    
    // 指定类型的属性构成的对象
    optionalObjectOf: React.PropTypes.objectOf(React.PropTypes.number),
    
    // 特定 shape 参数的对象
    optionalObjectWithShape: React.PropTypes.shape({
        color: React.PropTypes.string,
        fontSize: React.PropTypes.number
    }),
    
    // 任意类型加上 `isRequired` 来使 prop 不可空。
    requiredFunc: React.PropTypes.func.isRequired,
    
    // 不可空的任意类型
    requiredAny: React.PropTypes.any.isRequired,
 
    // 自定义验证器。如果验证失败需要返回一个 Error 对象。不要直接使用 `console.warn` 或抛异常，因为这样 `oneOfType` 会失效。
    customProp: function(props, propName, componentName) {
      if (!/matchme/.test(props[propName])) {
        return new Error('Validation failed!');
      }
    }
  }
}
```

## React 事件处理

> React 元素的事件处理和 DOM 元素类似。但是有一点语法上的不同:
>
> - React 事件绑定属性的**命名采用驼峰式写法**，而不是小写。
> - 如果采用 JSX 的语法你需要传入一个函数作为事件处理函数，而不是一个字符串(DOM 元素的写法)
> - 不能使用返回 false 的方式阻止默认行为， 你必须**明确的使用 preventDefault**。

```react
## 按钮
<button onClick={ activateLasers }>按钮</button>
## 链接
function ActionLink(){
    function handleClick(e){
        e.preventDefault();		// e是一个合成事件
    }
    return(
    	<a herf="#" onClick={ handleClick } >链接</a>
    );
}
```

> 使用 React 的时候通常你不需要使用 addEventListener 为一个已创建的 DOM 元素添加监听器。你仅仅需要**在这个元素初始渲染的时候提供一个监听器**。
>
> 当你使用 ES6 class 语法来定义一个组件的时候，事件处理器会成为类的一个方法。
>
> **在以类继承的方法定义的组件中，事件处理函数的this指向的并不是当前组件。**

```react
## Toggle 组件渲染一个让用户切换开关状态的按钮
class Toggle extends Reat.Component{
    constructor(props){
        super(props);
        this.state = { isToggleOn: true };
        // 必要绑定：绑定后 `this` 才能在回调函数中使用
        this.handleClick = this.handleClick.bind(this);
    }
    handleClick(){
        this.setState(prevState => ({
            isToggleOn: !prevState.isToggleOn
        }));
    }
    render(){
        return (
        	<button onClick={this.handleClick}>
            	{ this.state.isToggleOn ? 'ON' : 'OFF' }
            </button>
        );
    }
}

ReactDOM.render(
  <Toggle />,
  document.getElementById('example')
);
```

> 类的方法默认不绑定 this 。
>
> 如果忘记绑定 this.handleClick 并把它传入 onClick，当调用这个函数的时候 this 的值会是 undefined。
>
> 通常情况下，如果没有在方法后面添加 () ，例如 **onClick={this.handleClick}**，应该为这个方法绑定 this。
>
> **bind方式（仅为测试方法）：**
>
> 1. **通过bind方法进行原地绑定，从而改变this指向**
> 2. **在constructor中提前对事件进行绑定**

```react
## 方法 - 1：bind方法原地绑定
class LoggingButton extends React.Component {
	handleClick(){
        console.log('this is:', this);
    }
    render() {
        return (
            <button onClick={this.handleClick.bind(this)}>Click me</button>
        );
    }
}
## 方法 - 2：在constructor中提前对事件进行绑定
class LoggingButton extends React.Component {
    constructor(props){
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }
	handleClick(){
        console.log('this is:', this);
    }
    render() {
        return (
            <button onClick={this.handleClick}>Click me</button>
        );
    }
}
```

> **以下有两种替代bind的方式（仅为测试方法）：**
>
> 1. **使用属性初始化器语法**
> 2. **在回调函数中使用箭头函数**

```react
## 方法 - 1：如果正在使用实验性的属性初始化器语法，可以使用属性初始化器来正确的绑定回调函数
class LoggingButton extends React.Component {
    // 这个语法确保了 `this` 绑定在  handleClick 中
	handleClick = () => {
        console.log('this is:', this);
    }
    // 也可以在此处采用箭头函数写法
    handleClick = (e) => {
        e.preventDefault();
        console.log('this is:', this);
    }
    render() {
        return (
            <button onClick={this.handleClick}>Click me</button>
        );
    }
}
## 方法 - 2：如果没有使用属性初始化器语法，可以在回调函数中使用箭头函数
class LoggingButton extends React.Component{
    handleClick(){
        console.log('this is:', this);
    }
    render(){
        //  这个语法确保了 `this` 绑定在  handleClick 中
        return (
            <button onClick={(e) => this.handleClick(e)}>Click me</button>
        );
    }
}
```

**向事件处理程序传递参数**

> 通常我们会为事件处理程序传递额外的参数。
>
> 例如，若是 id 是你要删除那一行的 id，以下两种方式都可以向事件处理程序传递参数。

```react
<button onClick={ (e) => this.deleteRow(id, e) } >Delete Row</button>
<button onClick={ this.deleteRow.bind(this, id) } >Delete Row</button>
```

> 上面两个例子中，参数 e 作为 React 事件对象将会被作为第二个参数进行传递。
>
> 通过**箭头函数**的方式，**事件对象必须显式的进行传递**。
>
> 通过 **bind** 的方式，**事件对象以及更多的参数将会被隐式的进行传递**。
>
> 值得注意的是，通过 bind 方式向监听函数传参，在类组件中定义的监听函数，事件对象 e 要排在所传递参数的后面。

```react
class Popper extends React.Component{
    constructor(){
        super();
        this.state = { parameter: 'parameter' };
    }
    // 事件对象e放在最后
    preventPop(parameter, e){
        e.preventDefault();
        alert(parameter);
    }
    render(){
        return (
            // 通过箭头函数
            <a  herf="#"
                onClick={(e)=>this.preventPop(parameter, e)}>
                链接点击
            </a>
            // 通过 bind() 方法传递参数
            <a  herf="#" 
                onClick={this.preventPop.bind(this, parameter)}>
            	链接点击
            </a>
        );
    }
}
```

## React 条件渲染

> 在 React 中，可以创建不同的组件来封装各种需要的行为。然后还可以根据应用的状态变化只渲染其中的一部分。
>
> React 中的条件渲染和 JavaScript 中的一致，使用 JavaScript 操作符 if 或条件运算符来创建表示当前状态的元素，然后让 React 根据它们来更新 UI。

```react
## 两个组件
function UserGreeting(props) {
    return <h1>欢迎回来!</h1>;
}
function GuestGreeting(props) {
    return <h1>请先注册。</h1>;
}
## 创建一个 Greeting 组件，它会根据用户是否登录来显示其中之一
function Greeting(props) {
    const isLoggedIn = props.isLoggedIn;
    if (isLoggedIn) {
        return <UserGreeting />;
    }
    return <GuestGreeting />;
}

ReactDOM.render(
    <Greeting isLoggedIn={false} />,
    document.getElementById('example')
);
```

**元素变量**

> 可以使用变量来储存元素。
>
> 它可以帮助你有条件的渲染组件的一部分，而输出的其他部分不会更改。

```react
class LoginControl extends React.Component{
    constructor(props){
        super(props);
        this.handleLoginClick = this.handleLoginClick.bind(this);
        this.handleLogoutClick = this.handleLogoutClick.bind(this);
        this.state = { isLogin : false };
    }
    handleLoginClick(){
        this.setState({ isLogin: true });
    }
    handleLogoutClick(){
        this.setState({ isLogin: false });
    }
    render(){
        const isLogin = this.state.isLogin;
        let button = null;
        if(isLogin){
            button = <LogoutButton onClick={this.handleLogoutClick} />
        }else{
            button = <LoginButton onClick={this.handleLoginClick} />
        }
        return(
        	<div>
            	<Greeting isLoggedIn={isLogin} />
                {button}
            </div>
        );
    }
}

ReactDom.render(
	<LoginControl />,
    document.getElementById('example')
);
```

**与运算符 &&**

> 可以通过用花括号包裹代码在 JSX 中嵌入任何表达式 ，也包括 JavaScript 的逻辑与 &&，它可以方便地条件渲染一个元素。
>
> 在 JavaScript 中，**true && expression** 总是返回 **expression**，而 **false && expression** 总是返回 **false**。
>
> 因此，如果条件是 **true**，则 **&&** 右侧的元素就会被渲染，如果条件是 **false**，React 会忽略并跳过它。

**三目运算符**

```react
condition ? true : false
```

**阻止组件渲染**

> 在极少数情况下，你可能希望隐藏组件，即使它被其他组件渲染。让 render 方法返回 null 而不是它的渲染结果即可实现。
>
> 组件的 render 方法返回 null 并不会影响该组件生命周期方法的回调。
>
> 例如，componentWillUpdate 和 componentDidUpdate 依然可以被调用。

```react
function WarningBanner(props) {
    if (!props.warn) {
        return null;
    }
    return (
        <div className="warning">警告!</div>
    );
}
class Page extends React.Component {
    constructor(props) {
        super(props);
        this.state = { showWarning: true }
        this.handleToggleClick = this.handleToggleClick.bind(this);
    }
    handleToggleClick() {
        this.setState(prevState => ({
            showWarning: !prevState.showWarning
        }));
    }
    render() {
        return (
            <div>
                <WarningBanner warn={this.state.showWarning} />
                <button onClick={this.handleToggleClick}>
                    {this.state.showWarning ? '隐藏' : '显示'}
                </button>
            </div>
        );
    }
}
 
ReactDOM.render(
    <Page />,
    document.getElementById('example')
);
```

## React列表 & Keys

> 使用 JavaScript 的 map() 方法来创建列表

```react
const numbers = [1, 2, 3, 4, 5];
const listItems = numbers.map( (numbers) => <li>{numbers}</li> );
ReactDOM.render(
	<ul>{listItems}</ul>,
    document.getElementById('example')
);
## 将以上实例重构成一个组件，组件接收数组参数，每个列表元素分配一个 key
function NumberList(props) {
    const numbers = props.numbers;
    const listItems = numbers.map(
        (number) => <li key={number.toString()}>{number}</li>
    );
    return (
        <ul>{listItems}</ul>
    );
}
 
const numbers = [1, 2, 3, 4, 5];
ReactDOM.render(
	<NumberList numbers={numbers} />,
    document.getElementById('example')
};
```

**Keys**

> Keys 可以在 DOM 中的某些元素被增加或删除的时候帮助 React 识别哪些元素发生了变化。因此你应当给数组中的每一个元素赋予一个确定的标识。
>
> 一个元素的 key 最好是这个元素在列表中拥有的一个独一无二的字符串。通常，我们使用来自数据的 id 作为元素的 key。
>
> 当元素没有确定的 id 时，你可以使用他的序列号索引 index 作为 key。
>
> 如果列表可以重新排序，我们不建议使用索引来进行排序，因为这会导致渲染变得很慢。

```react
// 元素的确定id作为key
const todoItemsId = todos.map(
    (todo) => <li key={todo.id}>{todo.text}</li>
);
// 元素序列号索引index作为key
const todoItemsIdx = todos.map(
    (todo, index) => <li key={index}>{todo.text}</li>
);
```

**用keys提取组件**

> 元素的 key 只有在它和它的兄弟节点对比时才有意义。比如，如果你提取出一个 ListItem 组件，你应该把 key 保存在数组中的这个 **<ListItem />** 元素上，而不是放在 ListItem 组件中的 **<li>** 元素上。
>
> 在 map() 方法的内部调用元素时，最好为每一个元素加上一个独一无二的 key。

```react
function ListItem(props) {
    // 这里不需要指定key
    return <li>{props.value}</li>;
}
function NumberList(props) {
    const numbers = props.numbers;
    const listItems = numbers.map(
		// key应该在数组的上下文中被指定
        (number) => <ListItem key={number.toString()} value={number} />
    );
    return (
        <ul>{listItems}</ul>
    );
} 
const numbers = [1, 2, 3, 4, 5];
ReactDOM.render(
  <NumberList numbers={numbers} />,
  document.getElementById('example')
);
```

**元素的 key 在他的兄弟元素之间应该唯一**

> 数组元素中使用的 key 在其兄弟之间应该是独一无二的。然而，它们不需要是全局唯一的。当我们生成两个不同的数组时，我们可以使用相同的键。

```react
function Blog(props) {
    const sidebar = (
        <ul>{props.posts.map((post) =>
        	<li key={post.id}>{post.title}</li>
     	)}
    	</ul>
    );
	const content = props.posts.map((post) =>
        <div key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.content}</p>
        </div>
    );
    return (
        <div>
            {sidebar}
            <hr />
            {content}
        </div>
    );
}

const posts = [
  {id: 1, title: 'Title-1', content: 'Content - 1'},
  {id: 2, title: 'Title-2', content: 'Content - 2'}
];
ReactDOM.render(
  <Blog posts={posts} />,
  document.getElementById('example')
);
```

> key 会作为给 React 的提示，但不会传递给组件。
>
> 如果组件中需要使用和 key 相同的值，请将其作为属性传递。

```react
## 下面例子中，Post 组件可以读出 props.id，但是不能读出 props.key。
const content = posts.map(
    (post) => <Post key={post.id} id={post.id} title={post.title} />
);
```

## React 组件API

> - 设置状态：setState
>
>   ```react
>   setState(object nextState[, function callback])
>   ```
>
>   **参数说明**
>
>   - **nextState**，将要设置的新状态，该状态会和当前的**state**合并
>   - **callback**，可选参数，回调函数。该函数会在**setState**设置成功，且组件重新渲染后调用。
>
>   > 合并nextState和当前state，并重新渲染组件。setState是React事件处理函数中和请求回调函数中触发UI更新的主要方法。
>
>   **关于setState**
>
>   >不能在组件内部通过this.state修改状态，因为该状态会在调用setState()后被替换。
>   >
>   >setState()并不会立即改变this.state，而是创建一个即将处理的state。setState()并不一定是同步的，为了提升性能React会批量执行state和DOM渲染。
>   >
>   >setState()总是会触发一次组件重绘，除非在shouldComponentUpdate()中实现了一些条件渲染逻辑。
>
> - 替换状态：replaceState
>
>   ```react
>   replaceState(object nextState[, function callback])
>   ```
>
>   **参数说明**
>
>   - **nextState**，将要设置的新状态，该状态会替换当前的**state**。
>   - **callback**，可选参数，回调函数。该函数会在**replaceState**设置成功，且组件重新渲染后调用。
>
>   > **replaceState()**方法与**setState()**类似，但是方法只会保留**nextState**中状态，原**state**不在**nextState**中的状态都会被删除。
>
> - 设置属性：setProps
>
>   ```react
>   setProps(object nextProps[, function callback])
>   ```
>
>   **参数说明**
>
>   - **nextProps**，将要设置的新属性，该状态会和当前的**props**合并
>   - **callback**，可选参数，回调函数。该函数会在**setProps**设置成功，且组件重新渲染后调用。
>
>   > 设置组件属性，并重新渲染组件。
>   >
>   > **props**相当于组件的数据流，它总是会从父组件向下传递至所有的子组件中。当和一个外部的JavaScript应用集成时，我们可能会需要向组件传递数据或通知**React.render()**组件需要重新渲染，可以使用**setProps()**。
>   >
>   > 更新组件，可以在节点上再次调用**React.render()**，也可以通过**setProps()**方法改变组件属性，触发组件重新渲染。
>
> - 替换属性：replaceProps
>
>   ```react
>   replaceProps(object nextProps[, function callback])
>   ```
>
>   **参数说明**
>
>   - **nextProps**，将要设置的新属性，该属性会替换当前的**props**。
>   - **callback**，可选参数，回调函数。该函数会在**replaceProps**设置成功，且组件重新渲染后调用。
>
>   > **replaceProps()**方法与**setProps**类似，但它会删除原有 props。
>
> - 强制更新：forceUpdate
>
>   ```react
>   forceUpdate([function callback])
>   ```
>
>   **参数说明**
>
>   - **callback**，可选参数，回调函数。该函数会在组件**render()**方法调用后调用。
>
>   >forceUpdate()方法会使组件调用自身的render()方法重新渲染组件，组件的子组件也会调用自己的render()。但是，组件重新渲染时，依然会读取this.props和this.state，如果状态没有改变，那么React只会更新DOM。
>   >
>   >forceUpdate()方法适用于this.props和this.state之外的组件重绘（如：修改了this.state后），通过该方法通知React需要调用render()
>   >
>   >一般来说，应该尽量避免使用forceUpdate()，而仅从this.props和this.state中读取状态并由React触发render()调用。
>
> - 获取DOM节点：findDOMNode
>
>   ```react
>   DOMElement findDOMNode()
>   ```
>
>   - 返回值：DOM元素DOMElement
>
>   > 如果组件已经挂载到DOM中，该方法返回对应的本地浏览器 DOM 元素。当**render**返回**null** 或 **false**时，**this.findDOMNode()**也会返回**null**。从DOM 中读取值的时候，该方法很有用，如：获取表单字段的值和做一些 DOM 操作。
>
> - 判断组件挂载状态：isMounted
>
>   ```react
>   bool isMounted()
>   ```
>
>   >**isMounted()**方法用于判断组件是否已挂载到DOM中。可以使用该方法保证了**setState()**和**forceUpdate()**在异步场景下的调用不会出错。

## React 组件生命周期

> **组件的生命周期可分成三个状态**：
>
> - Mounting：已插入真实 DOM
> - Updating：正在被重新渲染
> - Unmounting：已移出真实 DOM
>
> **生命周期的方法**：
>
> - **componentWillMount** 在渲染前调用,在客户端也在服务端。
> - **componentDidMount** : 在第一次渲染后调用，只在客户端。之后组件已经生成了对应的DOM结构，可以通过this.getDOMNode()来进行访问。 如果你想和其他JavaScript框架一起使用，可以在这个方法中调用setTimeout, setInterval或者发送AJAX请求等操作(防止异步操作阻塞UI)。
> - **componentWillReceiveProps** 在组件接收到一个新的 prop (更新后)时被调用。这个方法在初始化render时不会被调用。
> - **shouldComponentUpdate** 返回一个布尔值。在组件接收到新的props或者state时被调用。在初始化时或者使用forceUpdate时不被调用。
>   可以在你确认不需要更新组件时使用。
> - **componentWillUpdate**在组件接收到新的props或者state但还没有render时被调用。在初始化时不会被调用。
> - **componentDidUpdate** 在组件完成更新后立即调用。在初始化时不会被调用。
> - **componentWillUnmount**在组件从 DOM 中移除之前立刻被调用。

```react
## 以下实例在 Func 组件加载以后，通过 componentDidMount 方法设置一个定时器
## 每隔100毫秒重新设置组件的透明度，并重新渲染
## opacity：透明度
class Func extends React.Component{
    constructor(props){
        super(props);
        this.state = { opacity: 1.0 };
    }
    componentDidMount(){
        this.timer = setInterval(function(){
            var opacity = this.state.opacity;
            opacity -= .05;
            if(opacity < 0.1){
                opacity = 1.0;
            }
            this.setState({ opacity: opacity });
        }.bind(this), 100);
    }
    render(){
        return(
        	<div style={{opacity: this.state.opacity}}>
                { this.props.funcName }
            </div>
        );
    }
}

ReactDom.render(
	<Func funcName="func" />,
    document.body
);
```

```react
## 以下实例初始化 state ， setNewnumber 用于更新 state。
## 所有生命周期在 Content 组件中。
class Button extends React.Component{
    constructor(props){
        super(props);
        this.state = { data: 0 };
        this.setNewNumber = this.setNewNumber.bind(this);
    }
    setNewNumber(){
        this.setState({ data: this.state.data + 1 });
    }
    render(){
        return(
        	<div>
            	<button onClick={this.setNewNumber}>increment</button>
                <Content myNumber={this.state.data} />
            </div>
        );
    }
}
class Content extends React.Component{
    componentWillMount() {
        console.log('Component WILL MOUNT!')
    }
    componentDidMount() {
        console.log('Component DID MOUNT!')
    }
    componentWillReceiveProps(newProps) {
        console.log('Component WILL RECEIVE PROPS!')
    }
    shouldComponentUpdate(newProps, newState) {
        return true;
    }
    componentWillUpdate(nextProps, nextState) {
        console.log('Component WILL UPDATE!');
    }
    componentDidUpdate(prevProps, prevState) {
        console.log('Component DID UPDATE!')
    }
    componentWillUnmount() {
        console.log('Component WILL UNMOUNT!')
    }
    render() {
        return ( <h3>{this.props.myNumber}</h3> );
    }
}

ReactDOM.render(
	<Button />,
    document.getElementById('example')
);
```

## React AJAX

>React 组件的数据可以通过 **componentDidMount** 方法中的 Ajax 来**获取**，当从服务端获取数据时可以将数据存储在 state 中，再用 this.setState 方法重新渲染 UI。
>
>当使用异步加载数据时，在组件卸载前使用 **componentWillUnmount** 来**取消**未完成的请求。

```react
class UserGist extends React.Component {
    constructor(props) {
        super(props);
        this.state = { username: '', lastGistUrl: '' };
    }
    componentDidMount() {
        this.serverRequest = $.get(this.props.source, function (result) {
            var lastGist = result[0];
            this.setState({
                username: lastGist.owner.login,
                lastGistUrl: lastGist.html_url
            });
        }.bind(this));
    }
    componentWillUnmount() {
        this.serverRequest.abort();
    }
    render() {
        return (
            <div>
                {this.state.username} 用户最新的 Gist 共享地址：
                <a href={this.state.lastGistUrl}>
                    { this.state.lastGistUrl }
                </a>
            </div>
        );
    }
}

ReactDOM.render(
    <UserGist source="https://api.github.com/users/octocat/gists" />,
    document.getElementById('example')
);
```

## React 表单与事件

> 在React中，可变的状态通常保存在组件的状态属性中，并且只能用 setState() 方法进行更新。

**简单实例 - 1：设置 input 值 value = {this.state.data}，在它发生变化时更新 state** 。

> 可以使用 **onChange** 事件来监听 input 的变化，并修改 state。
>
> 下面的代码将渲染出一个值为 value 的 input 元素，并通过 onChange 事件响应更新用户输入的值。

```react
class Func extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: 'value' };
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
        this.setState({ value: event.target.value });
    }
    render() {
        var value = this.state.value;
        return (
            <input type="text" value={value} onChange={this.handleChange} /> 
        ); 
    }
}

ReactDOM.render(
  <Func />,
  document.getElementById('example')
);
```

**简单实例 - 2：在子组件上使用表单**

> **onChange** 方法将触发 state 的更新并将更新的值传递到子组件的输入框的 **value** 上来重新渲染界面。
>
> 需要在父组件通过创建事件句柄 (**handleChange**) ，并作为 prop (**updateStateProp**) 传递到子组件上。

```react
class Content extends React.Component{
    render(){
        return (
        	<input type="text" value={this.props.myDataProp}
                   onChange={this.props.updateStateProp} /> 
        );
    }
}
class Func extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: 'value' };
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
        this.setState({ value: event.target.value });
    }
    render() {
        var value = this.state.value;
        return (
            <Content myDataProp = {value} 
                     updateStateProp = {this.handleChange} />
        ); 
    }
}

ReactDOM.render(
	<Func />,
    document.getElementById('example')
);
```

**Select 下拉菜单**

> 在 React 中，不使用 selected 属性，而在根 select 标签上用 value 属性来表示选中项。

```react
class FlavorForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: 'value' };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleChange(event) {
        this.setState({ value: event.target.value });
    }
    handleSubmit(event) {
        alert('Your favorite flavor is: ' + this.state.value)
    }
    render() {
        return (
        	<form onSubmit={this.handleSubmit}>
            	<label>选择喜欢的网站
                	<select value={this.state.value}
                            onChange={this.handleChange}>
                    	<option value='tb'>taobao</option>
                        <option value='fb'>facebook</option>
                    </select>
                </label>
                <input type="submit" value='submit' />
            </form>
        );
    }
}

ReactDOM.render(
	<FlavorForm />,
    document.getElementById('example')
);
```

**多个表单**

> 当有处理多个 input 元素时，可以通过给每个元素添加一个 name 属性，来让处理函数根据 **event.target.name** 的值来选择做什么。

```react
class Reservation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isGoing: true,
            numberOfGuests: 2
        }; 
        this.handleInputChange = this.handleInputChange.bind(this);
    }
    handleInputChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        this.setState({
            [name]: value
        });
    }
    render() {
        return (
            <form>
                <label>是否离开:
                    <input name="isGoing"
                           type="checkbox"
                           checked={this.state.isGoing}
                           onChange={this.handleInputChange} />
                </label>
                <br />
                <label>访客数:
                    <input name="numberOfGuests"
                           type="number"
                           value={this.state.numberOfGuests}
                           onChange={this.handleInputChange} />
                </label>
            </form>
        );
    }
}
```

**React 事件：通过onClick事件修改数据**

```react
class Func extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: 'value' };
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
        this.setState({ value: 'new value' });
    }
    render() {
        var value = this.state.value;
        return (
            <div>
            	<button onClick={this.handleChange}>按钮点击</button>
                <h2>{value}</h2>
            </div>
            
        ); 
    }
}

ReactDOM.render(
  <Func />,
  document.getElementById('example')
);
```

> 当需要从子组件中更新父组件的 **state** 时，需要在父组件通过创建事件句柄 (**handleChange**) ，并作为 prop (**updateStateProp**) 传递到子组件上。

```react
class Content extends React.Component{
    render(){
        return (
            <div>
                <button onClick = {this.props.updateStateProp}>点击</button>
                <h4>{this.props.myDataProp}</h4>
           </div>
        );
    }
}
class Func extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: 'value' };
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
        this.setState({ value: 'new value' });
    }
    render() {
        var value = this.state.value;
        return (
            <Content myDataProp = {value} 
                     updateStateProp = {this.handleChange} />
        ); 
    }
}

ReactDOM.render(
	<Func />,
    document.getElementById('example')
);
```

## React Refs

> React 支持一种非常特殊的属性 **Ref** ，可以用来绑定到 render() 输出的任何组件上。
>
> 这个特殊的属性允许引用 render() 返回相应的支撑实例（ backing instance ）。这样就可以确保在任何时间总是拿到正确的实例。

**使用方法**

```react
## 绑定一个 ref 属性到 render 的返回值上
<input ref="myInput" />

## 在其它代码中，通过 this.refs 获取支撑实例
var input = this.refs.myInput;
var inputValue = input.value;
var inputRect = input.getBoundingClientRect();
```

**完整实例**

> 通过使用 this 来获取当前 React 组件，或使用 ref 来获取组件的引用

```react
class MyComponent extends React.Component {
    constructor(props) {
        super(props);
        this.myRef = React.createRef();
    }
    render() {
        return <div ref={this.myRef} />;
    }
}
```

## React 错误边界

> 默认情况下，若一个组件在渲染期间（render）发生错误，会导致整个组件树全部被卸载。
>
> 错误边界：是一个组件，该组件会捕获到渲染期间（render）子组件发生的错误，并有能力阻止错误继续传播。

**组件中添加捕获错误**

> 1. 编写生命周期函数 getDerivedStateFromError
>
>    1. 该函数为静态函数 `static getDerivedStateFromError`
>
>    2. 运行时间点：子组件被渲染发生错误之后且页面更新之前
>
>    3. 只有子组件发生错误时，该函数才会被执行
>
>    4. 该函数返回一个对象，React会将该对象的属性覆盖掉当前组件的state
>
>    5. 参数：错误对象
>
>    6. 通常该函数用于改变状态值
>
>       ```react
>       class ErrorBound extends React.Component {
>           this.state = { hasError:false }
>       	// 该函数为静态函数
>           static getDerivedStateFromError(error){
>               // 返回的值会自动 调用setState，将值和state合并
>               return { hasError:true }
>           }
>           render(){
>               if(this.state.hasError){
>                   return null
>               }
>               return this.props.children
>           }
>       }
>       ```
>
> 2. 编写生命周期函数 componentDidCatch




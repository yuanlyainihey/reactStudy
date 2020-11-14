## 环境搭建 

**准备**

```
Node.js			https://nodejs.org/en/	
yarn			https://yarnpkg.com/zh-Hans/docs/install
```

**检测node是否安装成功**

```
npm -v		|		npx -v
```

**安装cnpm**

```
npm install -g cnpm --registry=https://registry.npm.taobao.org
cnpm -v
```

**项目创建**

```
npm install create-react-app yarn -g
create-react-app project_name		// 项目名称不能有大写字母
yarn add antd --save				// 安装antdesign
npm install --save @ant-design/icons
```

**包&依赖安装**

```
yarn add packageName
```

**项目启动**

```
yarn run start		|		yarn start
```

**antd组件引用**

```
import {Input} from 'antd'
import 'antd/dist/antd.css'
```

## 项目流程

> - src
>
>   > - components
>   >   - StandardTable
>   >   - TableAddForm
>   >   - ErrorBoundary.js
>   >   - PageHeaderWrapper.js
>   >   - TableUploadForm.js
>   > - layouts
>   >   - BaseApp.js
>   >   - Header.js
>   >   - UserLayout.js
>   > - store
>   >   - login
>   >     - login.action.js
>   >     - login.redux.js
>   >     - login.saga.js
>   >     - service.js
>   >   - register
>   >   - createElection
>   >   - createElectionAdmin
>   >   - myElection
>   >   - myElectionAdmin
>   >   - fetchBbs
>   >   - fetchVotes
>   >   - index.js
>   >   - sagas.js
>   >   - selectors.js
>   > - views
>   >   - login
>   >     - index.js
>   >   - register
>   >   - registerResult
>   >   - updateUser
>   >   - createElection
>   >     - index.js
>   >     - components
>   >   - createElectionAdmin
>   >   - myElection
>   >   - myElectionAdmin
>   >   - myVerifyVote
>   >   - electionDetail
>   >   - votersElection
>   >   - Main.js
>   >   - NotFound.js
>   > - App.js
>   > - cookie.js
>   > - index.js
>   > - serviceWorker.js
>   > - setupProxy.js

## config-overrides文件配置

> 通过react脚手架[create-react-app]创建的项目，如果需要在项目中配置一些webpack配置，需要在根目录下新建一个名称为config-overrides.js的文件。

**一、配置步骤：**

1. **引入react-app-rewired插件**

   react-app-rewired的作用就是在不eject的情况下,覆盖create-react-app的配置

2. **安装customize-cra，babel-plugin-import**

3. **修改 package.json 里的启动配置**

   ```react
   /* package.json */
   "scripts": {
   -   "start": "react-scripts start",
   +   "start": "react-app-rewired start",
   -   "build": "react-scripts build",
   +   "build": "react-app-rewired build",
   -   "test": "react-scripts test --env=jsdom",
   +   "test": "react-app-rewired test --env=jsdom",
   }
   ```

**二、应用步骤**

1. 配置文件路径别名

   ```react
   const { override, addWebpackAlias} = require('customize-cra');
   const path = require('path')
   
    module.exports = override(
      addWebpackAlias({
        assets: path.resolve(__dirname, './src/assets'),
        components: path.resolve(__dirname, './src/components'),
        pages: path.resolve(__dirname, './src/pages'),
        common: path.resolve(__dirname, './src/common')
      })
   );
   ```

2. 在开发过程中，我们经常会用到***Ant Design Mobile\***这个组件库，在引入组件的同时，往往还需要引入组件的css样式，如果每次都单独引入就比较麻烦，我们可以在config-overrides文件下全局配置一下。

   ```react
   const { override, fixBabelImports} = require('customize-cra');
   
    module.exports = override(
      fixBabelImports('import', {
        libraryName: 'antd-mobile',
        style: 'css',
      }),
   );
   ```

   ## others
   
   ```react
   const formItemLayout = {
   	labelCol: { span: 4 },  // 左边留白大小
   	wrapperCol: { span: 17 },  // 内容区大小（两者和不能!>24）
   };
   ```

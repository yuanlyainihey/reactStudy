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


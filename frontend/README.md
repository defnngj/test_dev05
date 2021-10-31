# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run your end-to-end tests
```
npm run test:e2e
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).



* 父组件与子组件

`:showStatus="showDailog"`
父组件`showDailog` 给到子组件`showStatus`

`@cancel="cancelProject"`
子组件的`cancel` 给到父组件`cancelProject`

:abc="aaa"  aaa 一定是个变量 aaa=120px
abc="aaa"   aaa 字符串
@abc="aaa"  aaa  是一个方法 aaa(){}

<template>
  <div id="app">
    <div id="nav">
      <!-- <router-link to="/">Home</router-link> | -->
      <!-- <router-link to="/about">About</router-link> -->
      <Navigation></Navigation>
    </div>
  </div>
</template>


<script>
import Navigation from '@/views/Navigation.vue'

export default {
  name: 'Home',
  components: {
    Navigation
  },
  data() {
    return {
      //
    }
  },
}

</script>

<style>
body {
  margin: 0px 0px 0px;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}

html,
body {
  height: 100%;
}

#nav {
  /* padding: 30px; */
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>

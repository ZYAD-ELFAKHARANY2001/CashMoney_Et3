

<template>
  <div class="greetings">
    <img alt="Vue logo" class="logo" src="../assets/initial-letter-mc-logo-or-cm-logo-vector-design-template-2BACWG6.jpg" width="125" height="125" />
    <h1>Sign Up</h1>
  </div>
  <div class="register">
    <input type="text" v-model="Username" placeholder="Enter Phone"/>
    <input type="text" v-model="Email" placeholder="Enter Email"/>
    <input type="Password" v-model="Password" placeholder="Enter Password"/>
    <input type="Password" v-model="PasswordConfirm" placeholder="Enter Confirm Password"/>
    <button @click="SignUp">Sign Up</button>

  </div>
</template>
<script> 
import axios from 'axios'
export default {
  name: 'SignUp',
  data(){
    return{
      Username:'',
      Email:'',
      Password:'',
      PasswordConfirm:'',
    }
  },methods:{
    SignUp(){
      if(this.Password==this.PasswordConfirm){
        axios.post('http://127.0.0.1:8000/register',{
          Username:this.Username,
          Email:this.Email,
          Password:this.Password,
        })
      .then(response=>{
          console.log(response);
        })
      .catch(error=>{
          console.log(error);
        })
      }
      else{
        alert('Passwords do not match');
      }
    }
  }
}
</script>
<style scoped>
.logo
{
  width: 125px;
  height: 125px;
}
.register input
{
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-right: auto;
  margin-left: auto;
  margin-bottom: 30px;
  border: 1px solid skyblue;
  border-radius: 4px;

}
.register button
{
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-right: auto;
  margin-left: auto;
  margin-bottom: 30px;
  border: 1px solid skyblue;
  background-color: skyblue;
  border-radius: 4px;
  cursor: pointer;
}
</style>

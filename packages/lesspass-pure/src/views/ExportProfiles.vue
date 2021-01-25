<template>
  <div>
    <h5>{{$t('Export Password Profiles')}}</h5>
    <form id="lesspass-options-form" novalidate v-on:submit.prevent="exportPasswordProfiles">
      <div class="form-group row">
        <div class="col-12">
          <div class="inner-addon left-addon">
            <i class="fa fa-user"></i>
            <input
              id="email"
              class="form-control"
              name="username"
              type="email"
              autocapitalize="none"
              v-bind:placeholder="$t('Email')"
              required
              v-model="email"
            />
          </div>
        </div>
      </div>
      <div class="form-group mb-2">
        <master-password
          v-model="masterPassword"
          v-bind:email="email"
          v-bind:label="$t('Master Password')"
          v-bind:showEncryptButton="true"
          v-bind:EncryptButtonText="$t('Encrypt my master password')"
          required
        ></master-password>
      </div>
      <button type="submit" id="btn-submit-settings" class="btn btn-primary btn-block mt-4">{{$t('Export')}}</button>
    </form>
  </div>
</template>

<script>
import { mapState } from "vuex";
import MasterPassword from "../components/MasterPassword.vue";
import Encryption from "../services/encryption";

export default {
  data() {
    return {
      masterPassword: "",
      email: "",
    };
  },
  computed: {
    ...mapState(["passwords", "encryptedKey"]),
  },
  components: {
    MasterPassword
  },
  methods: {
    exportPasswordProfiles() {
      const data = JSON.stringify(this.passwords);
      const encryptedPasswordProfiles = Encryption.encrypt(
        data,
        this.encryptedKey
      );
      const key = Encryption.decrypt(this.encryptedKey, this.masterPassword);
      const content = {
        profiles: encryptedPasswordProfiles,
        key: key
      };
      const fileContent = JSON.stringify(content);
      console.log(fileContent);

      const e = document.createElement('a');
      e.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(fileContent));
      e.setAttribute('download', 'profiles.lp');
      e.style.display = 'none';
      document.body.appendChild(e);
      e.click();
      document.body.removeChild(e);
    }
  }
};
</script>

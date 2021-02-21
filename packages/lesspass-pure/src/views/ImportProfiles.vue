<template>
  <div>
    <h5>{{$t('Import Password Profiles')}}</h5>
    <form id="lesspass-options-form" novalidate v-on:submit.prevent="importPasswordProfiles">
      <div class="form-group">
        <label for="profiles">{{ $t('Upload Password Profiles') }}</label>
          <input
            id="profiles"
            type="file"
            name="profiles"
            ref="profiles"
            class="form-control-file"
            v-bind:placeholder="$t('Upload')"
            v-on:change="getFileContents"
          />
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
      <button type="submit" id="btn-submit-settings" class="btn btn-primary btn-block mt-4">{{$t('Import')}}</button>
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
      profiles: "",
      masterPassword: "",
      key: "",
    };
  },
  components: {
    MasterPassword
  },
  methods: {
    importPasswordProfiles() {
      const encryptedKey = Encryption.encrypt(
        this.key,
        this.masterPassword
      );
      const passwords = JSON.parse(
        Encryption.decrypt(this.profiles, encryptedKey)
      );
      this.$store.dispatch("setEncryptedKey", {
        encryptedKey
      });
      this.$store.dispatch("loadPasswordProfiles", passwords);
      this.$router.push({ name: "passwords" });
    },
    getFileContents(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
      var file = e.target.files[0]; 
      var reader = new FileReader();
      reader.readAsText(file,'UTF-8');
      reader.onload = readerEvent => {
        var content = JSON.parse(readerEvent.target.result);
        this.profiles = content["profiles"];
        this.key = content["key"];
      }
    }
  }
};
</script>

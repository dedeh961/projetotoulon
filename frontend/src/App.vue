<template>
  <div id="app">
    <EnviarCSV @arquivo_atualizado="atualizar_lista_de_arquivos_csv"/>
    <ListaDeArquivosCSV ref="lista_de_arquivos"/>
  </div>
</template>
  
<script>
  import EnviarCSV from './components/EnviarCSV.vue';
  import ListaDeArquivosCSV from './components/ListaDeArquivosCSV.vue';

  export default {
    components: {
      EnviarCSV,
      ListaDeArquivosCSV
    },
    methods: {
      atualizar_lista_de_arquivos_csv() {
        this.$refs.lista_de_arquivos.recuperar_arquivos();
      }
    }
  };
</script>

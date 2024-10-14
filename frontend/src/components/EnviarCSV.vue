<template>
  <div>
    <h2>Crie/Atualize um arquivo CSV</h2>
    <div class="area-soltar-arquivo" @dragover.prevent @drop.prevent="arquivo_dropado">
      <p v-if="!arquivo_selecionado">Puxe arquivos para aqui ou clique para buscar</p>
      <p v-if="arquivo_selecionado">Arquivo selecionado: {{ arquivo_selecionado.name }}</p>
      <input type="file" @change="resolver_atualizao_de_arquivo" />
    </div>
    <button class="enviar-arquivo" type="button" @click="enviar_arquivo">Enviar arquivo</button>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        arquivo_selecionado: null,
      };
    },
    methods: {
      arquivo_dropado(event) {
        this.arquivo_selecionado = event.dataTransfer.files[0];
      },
      resolver_atualizao_de_arquivo(event) {
        this.arquivo_selecionado = event.target.files[0];
      },
      async enviar_arquivo() {
        if (!this.arquivo_selecionado) {
          alert('Por favor, selecione um arquivo primeiro.');
          return;
        }

        const mapeamento_do_arquivo = new FormData();
        mapeamento_do_arquivo.append('file', this.arquivo_selecionado);
        
        try {
          const response = await axios.post('http://localhost:8000/EnviarCSV/', mapeamento_do_arquivo, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });

          alert(response.data.message);
          this.$emit('arquivo_atualizado');
        } catch (error) {
          console.error('Erro ao enviar o arquivo:', error);
        }
      }
    }
  };
</script>

<style scoped>
.area-soltar-arquivo {
  width: 100%;
  max-width: 600px;
  height: 200px;
  border: 2px dashed #4A90E2;
  border-radius: 10px;
  text-align: center;
  padding: 20px;
  margin: 20px 0;
  transition: background-color 0.3s;
  background-color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  position: relative;
}

.area-soltar-arquivo:hover,
.area-soltar-arquivo.drag-over {
  background-color: #e7f3ff;
}

.area-soltar-arquivo input[type="file"] {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  opacity: 0;
  cursor: pointer;
}

.enviar-arquivo {
  background-color: #4A90E2;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}
</style>

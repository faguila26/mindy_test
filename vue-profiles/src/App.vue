<template>
  <div id="app">
    <h1>Lista de Perfiles</h1>
    <div class="uk-container">
      <!-- Cuadrícula responsiva de UIkit -->
      <div class="uk-grid uk-grid-column-small uk-grid-row-large uk-child-width-1-4@m uk-child-width-1-1@s uk-grid-match" uk-grid>
        <!-- Iterar sobre los perfiles -->
        <div v-for="profile in profiles" :key="profile.email" class="uk-card uk-card-default uk-card-body uk-card-primary uk-margin-small">
          <h3 class="uk-card-title">{{ profile.email }}</h3>
          <p>Siguiente hora disponible: {{ profile.next_hour }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      profiles: []
    };
  },
  created() {
    this.obtenerProfiles();
  },
  methods: {
    async obtenerProfiles() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/profiles/');  // Ajusta esta URL a la de tu API Django
        this.profiles = response.data;
      } catch (error) {
        console.error('Hubo un error al obtener los perfiles:', error);
      }
    }
  }
};
</script>

<style scoped>


/* Estilo de las tarjetas */
.uk-card {
  background-color: #0083b7; /* Azul */
  color: rgb(255, 255, 255);
  margin-left: 20px; /* Margin left más pequeño para alinear las tarjetas */
  margin-right: 10px; /* Mantener margen derecho para espacio */
  margin-top: 10px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Para que el contenido se distribuya */
}


/* Estilo para los títulos de las tarjetas */
.uk-card-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

/* Estilo adicional para mejorar la presentación */
.uk-text-center {
  font-size: 2rem;
  font-weight: bold;
}


/* Puedes agregar más estilos aquí si es necesario */
</style>

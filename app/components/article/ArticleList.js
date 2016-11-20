import React, {Component} from 'react';
import Article from './Article';

import {Row, Col} from 'react-bootstrap/lib/';

// Remove the articles data from here, this is only for demo purposes.
const articles = [{
  src: 'http://www.el-nacional.com/politica/Delcy-Rodriguez-ONU-Foto-Cancilleria_NACIMA20161105_0024_19.jpg',
  title: 'Delcy Rodríguez asegura que la mayoría de los países aplaude logros de Venezuela en DD HH',
  category: 'Politica',
  date: '05/11/2016',
  text: 'La canciller de la República afirmó que en Venezuela nunca han sido violados los derechos de los ciudadanos. Reconoció que el  \'modelo de inclusión está en su punto más bajo\'',
  autorId: 1,
  likes: 6,
  comments: 10
},
  {
    src: 'http://www.el-nacional.com/politica/Delcy-Rodriguez-ONU-Foto-Cancilleria_NACIMA20161105_0024_19.jpg',
    title: 'Delcy Rodríguez asegura que la mayoría de los países aplaude logros de Venezuela en DD HH',
    category: 'Politica',
    date: '05/11/2016',
    text: 'La canciller de la República afirmó que en Venezuela nunca han sido violados los derechos de los ciudadanos. Reconoció que el  \'modelo de inclusión está en su punto más bajo\'',
    autorId: 1,
    likes: 6,
    comments: 10
  }, {
    src: 'http://www.el-nacional.com/politica/Delcy-Rodriguez-ONU-Foto-Cancilleria_NACIMA20161105_0024_19.jpg',
    title: 'Delcy Rodríguez asegura que la mayoría de los países aplaude logros de Venezuela en DD HH',
    category: 'Politica',
    date: '05/11/2016',
    text: 'La canciller de la República afirmó que en Venezuela nunca han sido violados los derechos de los ciudadanos. Reconoció que el  \'modelo de inclusión está en su punto más bajo\'',
    autorId: 1,
    likes: 6,
    comments: 10
  }, {
    src: 'http://www.el-nacional.com/politica/Delcy-Rodriguez-ONU-Foto-Cancilleria_NACIMA20161105_0024_19.jpg',
    title: 'Delcy Rodríguez asegura que la mayoría de los países aplaude logros de Venezuela en DD HH',
    category: 'Politica',
    date: '05/11/2016',
    text: 'La canciller de la República afirmó que en Venezuela nunca han sido violados los derechos de los ciudadanos. Reconoció que el  \'modelo de inclusión está en su punto más bajo\'',
    autorId: 1,
    likes: 6,
    comments: 10
  }, {
    src: 'http://www.el-nacional.com/politica/Delcy-Rodriguez-ONU-Foto-Cancilleria_NACIMA20161105_0024_19.jpg',
    title: 'Delcy Rodríguez asegura que la mayoría de los países aplaude logros de Venezuela en DD HH',
    category: 'Politica',
    date: '05/11/2016',
    text: 'La canciller de la República afirmó que en Venezuela nunca han sido violados los derechos de los ciudadanos. Reconoció que el  \'modelo de inclusión está en su punto más bajo\'',
    autorId: 1,
    likes: 6,
    comments: 10
  }, {
    src: 'http://www.el-nacional.com/politica/Delcy-Rodriguez-ONU-Foto-Cancilleria_NACIMA20161105_0024_19.jpg',
    title: 'Delcy Rodríguez asegura que la mayoría de los países aplaude logros de Venezuela en DD HH',
    category: 'Politica',
    date: '05/11/2016',
    text: 'La canciller de la República afirmó que en Venezuela nunca han sido violados los derechos de los ciudadanos. Reconoció que el  \'modelo de inclusión está en su punto más bajo\'',
    autorId: 1,
    likes: 6,
    comments: 10
  }, {
    src: 'http://www.el-nacional.com/politica/Delcy-Rodriguez-ONU-Foto-Cancilleria_NACIMA20161105_0024_19.jpg',
    title: 'Delcy Rodríguez asegura que la mayoría de los países aplaude logros de Venezuela en DD HH',
    category: 'Politica',
    date: '05/11/2016',
    text: 'La canciller de la República afirmó que en Venezuela nunca han sido violados los derechos de los ciudadanos. Reconoció que el  \'modelo de inclusión está en su punto más bajo\'',
    autorId: 1,
    likes: 6,
    comments: 10
}]

const articleComponent = article => (
  <Col xs={4} >
    <Article key={article.id} article={article} />
  </Col>
  )

export default class ArticleList extends Component {
  render () {
    return (
      <Row>
          {articles.map(article => articleComponent(article))}
      </Row>
    )
  }
}

ArticleList.propTypes = {
  articles: React.PropTypes.array,
  children: React.PropTypes.any
}
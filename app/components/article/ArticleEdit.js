import React, {Component} from 'react';
import { Grid, Row, Col } from 'react-bootstrap/lib/';
import { RaisedButton, TextField} from 'material-ui';
import { hashHistory } from 'react-router';

//Para la conexion con la api
import axios from 'axios';
		// "articleId": "este es el id del articulo",
		// "articlePosted": "aqui recibimos si este usuario aprobo el articulo (booleano)",
		// "articleKeyWords": "aqui ponemos las palabras claves del articulo"

const styles = {
	margin: 10
}

class ArticleEdit extends Component {
  constructor(props){
    super(props);
      this.state = {
       content: '',
       abstract: '',
       title: '',
       catgory: '',
       proceed: false
      }
      
		this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  enterEdit(response){
    this.setState({ proceed: true, title: '', content: '', catergory: '' , abstract: ''});
  }

  componentWillMount() {
    //verificar que se encuentre la sesion activa.
    axios.get('/user/info')
      .then(this.enterEdit);
  }

  handleChange(event) {
    if (this.state.proceed === true) {
      if (event.target.name === 'title') 
        this.setState({title: event.target.value, content: this.state.content, abstract: this.state.abstract, category: this.state.category})
      if (event.target.name === 'content')
        this.setState({title:  this.state.title, content:  event.target.value, abstract: this.state.abstract, category: this.state.category})
      if (event.target.name === 'abstract')
        this.setState({title: this.state.title, content: this.state.content, abstract: event.target.value, category: this.state.category})
      if (event.target.name === 'category')
        this.setState({title:  this.state.title, content: this.state.content, abstract: this.state.abstract, category: event.target.value})
    }
}

  handleSubmit(event) {
		event.preventDefault();
		let titleValue = event.target[0].value.trim();
		let contentValue = event.target[1].value.trim();
		let abstractValue = event.target[2].value.trim();
		let categoryValue = event.target[3].value.trim();
		let imageValue = event.target[4].value;

    axios.post('/article/post', {
			articleContent: contentValue,
      articleAbstract: abstractValue,
      articleTitle: titleValue,
      articleImage: imageValue,
      articleCatgory: categoryValue
		})
		.then(function (response) {
			console.log(response);
		})
		.catch(function (error) {
      console.log(error);
		});
		return;
	}

  render() {
    return (
      <Grid>
        <Row>
        <form onSubmit={this.handleSubmit}>
            <Col xs={12}>
              <TextField
                    name="text"
                    onChange={this.handleChange}
                    type="text"
                    value={this.state.text}
                    fullWidth={true}
                    hintText="Title of the article"
                    />
            </Col>
            <Col xs={12}>
              <TextField
                    name="content"
                    onChange={this.handleChange}
                    type="text"
                    value={this.state.text}
                    fullWidth={true}
                    hintText="Body of the article"
                    />
            </Col>
            <Col xs={12}>
              <TextField
                    name="category"
                    onChange={this.handleChange}
                    type="text"
                    value={this.state.text}
                    fullWidth={true}
                    hintText="Category of the article"
                    />
            </Col>
            <Col xs={12}>
                <input type="file" name="file" />
            </Col>
						<Col xs={10} xsOffset={1} md={4}>
							<RaisedButton type="submit" label="Submit" primary={true} style={styles} />
						</Col>
            </form>
          </Row>
				</Grid>
    );
  }
}

export default ArticleEdit;
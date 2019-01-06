import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import {WithContext as ReactTags} from 'react-tag-input';
import './style/css/bootstrap.min.css'
import './style/css/style.css'

const KeyCodes = {
    comma: 188,
    enter: 13,
};

const delimiters = [KeyCodes.enter];

class TagAdder extends Component{
    constructor(props) {
        super(props);

        this.state = {
            tags: [
                // { id: "Thailand", text: "Thailand" },
                // { id: "India", text: "India" }
            ],
            // suggestions: [
            //     { id: 'USA', text: 'USA' },
            //     { id: 'Germany', text: 'Germany' },
            //     { id: 'Austria', text: 'Austria' },
            //     { id: 'Costa Rica', text: 'Costa Rica' },
            //     { id: 'Sri Lanka', text: 'Sri Lanka' },
            //     { id: 'Thailand', text: 'Thailand' }
            // ]
        };
        this.handleDelete = this.handleDelete.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.handleDrag = this.handleDrag.bind(this);
    }

    handleDelete(i) {
        const { tags } = this.state;
        this.setState({
            tags: tags.filter((tag, index) => index !== i),
        });
    }

    handleAddition(tag) {
        this.setState(state => ({ tags: [...state.tags, tag] }));
    }

    handleDrag(tag, currPos, newPos) {
        const tags = [...this.state.tags];
        const newTags = tags.slice();

        newTags.splice(currPos, 1);
        newTags.splice(newPos, 0, tag);

        // re-render
        this.setState({ tags: newTags });
    }

    render() {
        const { tags } = this.state;
        return (
            <div className="card">
                <div className="card-header">{this.props.header}</div>
                <div className="card-body" id={this.props.id}>
                    <ReactTags tags={tags}
                               handleDelete={this.handleDelete}
                               handleAddition={this.handleAddition}
                               handleDrag={this.handleDrag}
                               delimiters={delimiters}
                               placeholder={this.props.placeholder}
                    />
                </div>
            </div>
    );
    }
}

function getCookie(name) {
    if (!document.cookie) {
        return null;
    }

    const xsrfCookies = document.cookie.split(';')
        .map(c => c.trim())
        .filter(c => c.startsWith(name + '='));

    if (xsrfCookies.length === 0) {
        return null;
    }

    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

class App extends Component {
    search(){
        let mustArray = [].slice.call(document.querySelectorAll('#must-tag > div > div > span')).map(x => x.innerText.replace('×', ''));
        let mustNotArray = [].slice.call(document.querySelectorAll('#must-not-tag > div > div > span')).map(x => x.innerText.replace('×', ''));
        let shouldArray = [].slice.call(document.querySelectorAll('#should-tag > div > div > span')).map(x => x.innerText.replace('×', ''));

        const http = new XMLHttpRequest();
        const url = "/search/";
        const params = JSON.stringify({
            mustArray: mustArray,
            mustNotArray: mustNotArray,
            shouldArray: shouldArray
        });
        http.open("POST", url, true);

        http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        http.onreadystatechange = function() {
            if(http.readyState === 4 && http.status === 200) {
                document.getElementById('search-result-area').innerText = http.responseText;
            }
        };

        const csrfToken = getCookie('csrftoken');
        http.setRequestHeader("X-CSRFToken", csrfToken);
        http.send(params);
    }
    render() {
        return (
            <div className="container container-fluid">
                <TagAdder id={'must-tag'} placeholder={"Add new must item"} header={'Must Items'}/>
                <TagAdder id={'must-not-tag'} placeholder={"Add new must not item"} header={'Must Not Items'}/>
                <TagAdder id={'should-tag'} placeholder={"Add new should item"} header={'Should Items'}/>
                <div className="button btn btn-success" id={"search-button"} onClick={this.search}>Search</div>
                <div className="card">
                    <div className="card-body multiple-space" id="search-result-area">

                    </div>
                </div>
            </div>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('app'));
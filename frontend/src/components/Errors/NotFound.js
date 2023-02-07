import { Alert, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import "./Errors.scss";

const NotFound = () => {
  return (
    <Alert variant="warning" className="centered message-box">
      <Alert.Heading className="header">PAGE NOT FOUND</Alert.Heading>
      <p>It looks like you got a wrong URL!</p>
      <Link to="/">
        <Button variant="outline-primary">Go back home</Button>
      </Link>
    </Alert>
  );
};

export default NotFound;

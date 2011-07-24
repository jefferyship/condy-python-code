package ecc.warning.pojo;

import java.util.HashMap;

public class JsonReturnObjectOfGwt extends HashMap {
	public void setError(Object object){
		put("error",object);
	}
	public void setResult(Object object){
		put("result",object);
	}
	public Object getError(){
		return get("error");
	}
	public Object getResult(){
		return get("result");
	}

}

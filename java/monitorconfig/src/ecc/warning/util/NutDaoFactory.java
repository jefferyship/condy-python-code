package ecc.warning.util;

import java.beans.PropertyVetoException;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.sql.DataSource;

import org.nutz.dao.impl.NutDao;

import com.mchange.v2.c3p0.ComboPooledDataSource;
import com.telthink.data.DatabaseConfig;
/**
 * 获取NutDao的静态工厂方法
 * @author 林桦
 *
 */
public class NutDaoFactory {
	public static NutDao getNutDaoInstance(){
		NutDao nutDao=null;
		try {
			nutDao= new NutDao(dataSource(null));
		} catch (NamingException e) {
			e.printStackTrace();
		}
		return nutDao;
	}
	public static NutDao getNutDaoInstance(String jndi) throws NamingException{
		NutDao nutDao=null;
		try {
			nutDao= new NutDao(dataSource(jndi));
		} catch (NamingException e) {
			e.printStackTrace();
		}
		return nutDao;
	}
	
	private static DataSource dataSource(String jndi) throws NamingException{
		 //使用J2EE环境中的DataSource
		String dataSourceName="";
		String driverName=DatabaseConfig.get(DatabaseConfig.DRIVER_NAME);
		if(driverName!=null&&!"".equals(driverName)){
			return getc3p0DataSource();
		}
		if(jndi==null||"".equals(jndi))
			dataSourceName=DatabaseConfig.get(DatabaseConfig.URL);
		else
			dataSourceName=jndi;
        DataSource ds=null;
        try {
            Context context=new InitialContext();
            ds=(DataSource) context.lookup(dataSourceName);
        } catch (Exception ex) {
            Context context=new InitialContext();
            context  = (Context)context.lookup("java:/comp/env");
            ds=(DataSource) context.lookup(dataSourceName);
            //ex.printStackTrace();
        }
        return ds;
	}
	
	private static DataSource getc3p0DataSource(){
		ComboPooledDataSource ds = new ComboPooledDataSource();
		try {
			ds.setDriverClass(DatabaseConfig.get(DatabaseConfig.DRIVER_NAME));
			ds.setJdbcUrl(DatabaseConfig.get(DatabaseConfig.URL));
			ds.setUser(DatabaseConfig.get(DatabaseConfig.USER));
			ds.setPassword(DatabaseConfig.get(DatabaseConfig.PWD));
			//ds.setMaxPoolSize(Integer.parseInt(DatabaseConfig.get(DatabaseConfig.MAX)));
			//ds.setMinPoolSize(Integer.parseInt(DatabaseConfig.get(DatabaseConfig.MIN)));

		} catch (PropertyVetoException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return ds;
	}

}

package ecc.warning.pojo;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Table;

@Table("MONITOR_ZX_ALARM_DETAIL_LOG")
public class ZxAlarmDetailLog {
	@Column("ALARM_SEQ")
	private String alarmSeq;
	@Column("ALARM_ITEM_ID")
	private String alarmItemId;
	@Column("ALARM_ITEM_VALUE")
	private String alarmItemValue;
	/**
	 * @return the alarmSeq
	 */
	public String getAlarmSeq() {
		return alarmSeq;
	}
	/**
	 * @param alarmSeq the alarmSeq to set
	 */
	public void setAlarmSeq(String alarmSeq) {
		this.alarmSeq = alarmSeq;
	}
	/**
	 * @return the alarmItemId
	 */
	public String getAlarmItemId() {
		return alarmItemId;
	}
	/**
	 * @param alarmItemId the alarmItemId to set
	 */
	public void setAlarmItemId(String alarmItemId) {
		this.alarmItemId = alarmItemId;
	}
	/**
	 * @return the alarmItemValue
	 */
	public String getAlarmItemValue() {
		return alarmItemValue;
	}
	/**
	 * @param alarmItemValue the alarmItemValue to set
	 */
	public void setAlarmItemValue(String alarmItemValue) {
		this.alarmItemValue = alarmItemValue;
	}
	

}
